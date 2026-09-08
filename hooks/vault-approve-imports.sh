#!/usr/bin/env bash
# vault-approve-imports.sh — hook plugin H3 · événement SessionStart · aussi CLI : vault-approve-imports.sh <dossier>…
#
# Approuve les imports externes du CLAUDE.md (`hasClaudeMdExternalIncludesApproved`) dans `~/.claude.json`
# pour un dossier de lancement, sans passer par le dialogue interactif « Allow external CLAUDE.md file imports? ».
#
# Pourquoi : Claude Code ignore en silence tout `@import` d'un CLAUDE.md projet dont la cible est hors du cwd
# de lancement, tant que ce dialogue n'a pas été accepté une fois pour ce cwd (anthropics/claude-code #79046,
# #87020, #88813 ; vérifié sur 2.1.259 le 2026-09-08). Une persona (`_personas/{slug}/`) ou un dossier de travail
# (`dossier-travail`) qui hérite du CLAUDE.md racine du vault est donc lancée sans Schema / governance / sources
# en mode -p, SDK ou Paseo, où le dialogue ne peut pas s'afficher.
#
# Garde-fou : on n'approuve QUE si chaque import externe se résout dans un vault (un dossier contenant `_Meta/`).
# Un CLAUDE.md qui importe autre chose hors du cwd n'est jamais approuvé ici : le dialogue reste la seule voie.
# Opt-out : `APPROVE_EXTERNAL_IMPORTS=0` dans `{vault}/_Meta/hooks.conf` du vault visé.
# Effet : à la PROCHAINE session dans ce dossier. Pour la session courante, le hook liste les fichiers non chargés
# pour que l'agent les lise à la demande.
#
# Modes : sans argument = hook (dossier = CLAUDE_PROJECT_DIR, sinon "cwd" du JSON stdin ; sortie JSON additionalContext).
#         avec arguments = CLI (un dossier par argument ; sortie texte). Jamais bloquant. Config : `~/.claude.json`,
#         ou `$CLAUDE_CONFIG_DIR/.claude.json` si la variable est posée. Écriture atomique. Dépendances : bash + python3.

. "$(dirname "$0")/vault-lib.sh"

if [ "$#" -gt 0 ]; then
  MODE=cli; TARGETS="$(printf '%s\n' "$@")"
else
  MODE=hook
  HOOK_INPUT="$(cat 2>/dev/null || true)"
  TARGETS="${CLAUDE_PROJECT_DIR:-}"
  [ -n "$TARGETS" ] || TARGETS="$(stdin_field cwd)"
  [ -n "$TARGETS" ] || exit 0
fi

MODE="$MODE" TARGETS="$TARGETS" python3 <<'PY'
import os, sys, re, json, tempfile

MODE = os.environ["MODE"]
HOME = os.path.expanduser("~")
cfg_dir = os.environ.get("CLAUDE_CONFIG_DIR", "").strip()
CFG = os.path.join(cfg_dir, ".claude.json") if cfg_dir else os.path.join(HOME, ".claude.json")
MAX_DEPTH = 5  # profondeur d'imports suivie par Claude Code

def say(msg):
    if MODE == "cli":
        print(msg)

def tilde(p):
    return "~" + p[len(HOME):] if p == HOME or p.startswith(HOME + os.sep) else p

def vault_root(path):
    d = path if os.path.isdir(path) else os.path.dirname(path)
    while d and d != os.path.dirname(d):
        if os.path.isdir(os.path.join(d, "_Meta")):
            return d
        d = os.path.dirname(d)
    return None

def conf(vault, key, default):
    f = os.path.join(vault, "_Meta", "hooks.conf")
    val = default
    try:
        for line in open(f, encoding="utf-8", errors="ignore"):
            m = re.match(r"\s*" + re.escape(key) + r"\s*=\s*([^#]*)", line)
            if m:
                val = m.group(1).strip()
    except OSError:
        pass
    return val

IMPORT_RE = re.compile(r"(?:^|(?<=\s))@([^\s`'\"<>()\[\]]+)")

def imports_of(md_path):
    """Chemins importés par un fichier .md (syntaxe `@chemin`), hors blocs et spans de code, normalisés (non realpath)."""
    try:
        text = open(md_path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return []
    out, fenced = [], False
    base = os.path.dirname(md_path)
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        line = re.sub(r"`[^`]*`", " ", line)
        for raw in IMPORT_RE.findall(line):
            raw = raw.rstrip(".,;:")
            if not raw:
                continue
            p = os.path.expanduser(raw) if raw.startswith("~") else raw
            p = p if os.path.isabs(p) else os.path.join(base, p)
            out.append(os.path.normpath(p))
    return out

def under(path, root):
    return path == root or path.startswith(root.rstrip(os.sep) + os.sep)

def analyse(cwd):
    """Imports externes (cibles hors du cwd, au sens littéral de Claude Code) atteints depuis les CLAUDE.md de cwd et ancêtres."""
    roots, d = [], cwd
    while True:
        roots.append(d)
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    seeds = []
    for r in roots:
        for name in ("CLAUDE.md", "CLAUDE.local.md", os.path.join(".claude", "CLAUDE.md")):
            f = os.path.join(r, name)
            if os.path.isfile(f):
                seeds.append(f)
    external, seen = [], set()

    def walk(f, depth):
        if depth > MAX_DEPTH:
            return
        for t in imports_of(f):
            if t in seen:
                continue
            seen.add(t)
            if not os.path.isfile(t):
                continue  # cible absente : Claude l'ignore aussi
            if not under(t, cwd):
                external.append(t)
                # au-delà du 1er niveau externe, Claude ne descend pas sans le flag : inutile d'aller plus loin
                continue
            walk(t, depth + 1)

    for s in seeds:
        walk(s, 1)
    return external

def approve(keys):
    try:
        with open(CFG, encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        say(f"ignoré : {tilde(CFG)} absent (Claude Code n'a jamais tourné ici)")
        return False
    except ValueError as e:
        say(f"ignoré : {tilde(CFG)} illisible ({e})")
        return False
    projects = data.setdefault("projects", {})
    changed = False
    for k in keys:
        p = projects.setdefault(k, {})
        if not p.get("hasClaudeMdExternalIncludesApproved"):
            p["hasClaudeMdExternalIncludesApproved"] = True
            p["hasClaudeMdExternalIncludesWarningShown"] = True
            changed = True
    if not changed:
        return False
    fd, tmp = tempfile.mkstemp(prefix=".claude.json.", dir=os.path.dirname(CFG))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
            fh.flush(); os.fsync(fh.fileno())
        try:
            os.chmod(tmp, os.stat(CFG).st_mode & 0o777)
        except OSError:
            pass
        os.replace(tmp, CFG)
    except Exception:
        try: os.unlink(tmp)
        except OSError: pass
        raise
    return True

notes = []
for raw in [t for t in os.environ["TARGETS"].splitlines() if t.strip()]:
    cwd = os.path.normpath(os.path.abspath(os.path.expanduser(raw.strip())))
    if not os.path.isdir(cwd):
        say(f"refusé : {tilde(cwd)} n'est pas un dossier"); continue
    external = analyse(cwd)
    if not external:
        say(f"rien à faire : {tilde(cwd)} n'a aucun import externe"); continue
    untrusted = [t for t in external if vault_root(os.path.realpath(t)) is None]
    if untrusted:
        say(f"refusé : {tilde(cwd)} importe hors d'un vault : " + ", ".join(tilde(t) for t in untrusted)
            + " (approuver via le dialogue interactif si c'est voulu)")
        continue
    vaults = sorted({vault_root(os.path.realpath(t)) for t in external})
    if any(conf(v, "APPROVE_EXTERNAL_IMPORTS", "1") in ("0", "false", "no", "non") for v in vaults):
        say(f"ignoré : APPROVE_EXTERNAL_IMPORTS=0 dans _Meta/hooks.conf de " + ", ".join(tilde(v) for v in vaults)); continue
    keys = [cwd]
    rp = os.path.realpath(cwd)
    if rp != cwd:
        keys.append(rp)
    if approve(keys):
        say(f"approuvé : {tilde(cwd)} (clé{'s' if len(keys) > 1 else ''} " + ", ".join(tilde(k) for k in keys)
            + f" dans {tilde(CFG)}) ; effet à la prochaine session. Imports : " + ", ".join(tilde(t) for t in external))
        notes.append((cwd, external))
    else:
        say(f"déjà approuvé : {tilde(cwd)}")

if MODE == "hook" and notes:
    cwd, external = notes[0]
    msg = ("Imports externes du CLAUDE.md approuvés pour " + tilde(cwd) + " (~/.claude.json) ; ils seront chargés "
           "à partir de la prochaine session. Non chargés dans cette session : " + ", ".join(tilde(t) for t in external)
           + ". Lis-les avant d'écrire ou de classer une fiche.")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": msg}}, ensure_ascii=False))
PY
exit 0
