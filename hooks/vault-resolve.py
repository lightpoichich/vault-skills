#!/usr/bin/env python3
"""vault-resolve.py — depuis un dossier quelconque, retrouve le vault et la fiche projet qui lui correspondent.

Utilisé par le hook Stop `vault-sync-nudge.sh` et par le skill `sync-repo` (règle de liaison, côté déterministe).

  vault-resolve.py [dossier]            → JSON  {"mode", "vault", "sheet", "repo", "subpath", "match"}
  vault-resolve.py --shell [dossier]    → lignes MODE=… VAULT=… SHEET=… REPO=… MATCH=… (à `eval`)

mode :
  vault  — le dossier est dans un vault (un ancêtre contient `_Meta/`) ; `sheet` vide.
  repo   — le dossier est dans un dépôt git hors vault, relié à une fiche `type: project` d'un vault.
  none   — ni l'un ni l'autre (pas de dépôt, pas de vault joignable, ou aucune fiche reliée).

Vault(s) candidats depuis un dépôt, dans l'ordre : cibles des `@imports` des CLAUDE.md du dossier et de ses
ancêtres (règle de liaison : le dépôt importe `@~/vault/…`), puis `~/.claude/CLAUDE.md` (ses `@imports` et tout
chemin absolu cité en clair, comme le « Le vault est à {VAULT_ABS} » du gabarit kickstart-vault), puis `~/vault`.
Fiche : dans `{vault}/10-Projects/`, par ordre de priorité —
  1. `repo:` = remote `origin` du dépôt (URL normalisée : sans schéma, sans `user@`, sans `.git`, insensible à la
     casse ; suffixe optionnel `#sous-dossier` quand le projet vit dans un sous-dossier du dépôt) ;
  2. `dossier-travail:` = le dossier (ou un de ses ancêtres jusqu'à la racine du dépôt) ;
  3. slug de la fiche = nom du dossier (ou de la racine du dépôt).
Dépendances : python3 + git. Jamais d'écriture.
"""
import os, re, sys, json, shlex, subprocess

HOME = os.path.expanduser("~")
IMPORT_RE = re.compile(r"(?:^|(?<=\s))@([^\s`'\"<>()\[\]]+)")


def vault_root(path):
    d = path if os.path.isdir(path) else os.path.dirname(path)
    while d and d != os.path.dirname(d):
        if os.path.isdir(os.path.join(d, "_Meta")):
            return d
        d = os.path.dirname(d)
    return None


def git(*args, cwd):
    try:
        r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=5)
    except Exception:
        return ""
    return r.stdout.strip() if r.returncode == 0 else ""


def repo_key(url):
    """Clé de comparaison d'une URL de dépôt : host/owner/name en minuscules. '' si vide."""
    u = (url or "").strip()
    if not u:
        return ""
    u = re.sub(r"^[a-z][a-z0-9+.-]*://", "", u, flags=re.I)   # schéma
    u = re.sub(r"^[^@/]+@", "", u)                            # user@
    if re.match(r"^[^/]+:", u):                               # scp-like host:owner/name
        u = u.replace(":", "/", 1)
    u = re.sub(r"\.git/?$", "", u).rstrip("/")
    return u.lower()


def imports_of(md_path):
    try:
        text = open(md_path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return []
    out, fenced, base = [], False, os.path.dirname(md_path)
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced; continue
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


PATH_RE = re.compile(r"(?<![\w@])(~|/)[^\s`'\"<>()\[\]{},;]+")


def paths_in(md_path):
    """Chemins absolus (ou ~/…) cités en clair dans un .md — le gabarit global de kickstart-vault écrit
    « Le vault (ta mémoire) est à {VAULT_ABS} » sans @import."""
    try:
        text = open(md_path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return []
    out = []
    for m in PATH_RE.finditer(text):
        raw = m.group(0).rstrip(".,;:")
        out.append(os.path.normpath(os.path.expanduser(raw)))
    return out


def candidate_vaults(d):
    """Vaults joignables depuis d, dédupliqués, du plus spécifique au plus général."""
    seeds, cur = [], d
    while True:
        for name in ("CLAUDE.md", "CLAUDE.local.md", os.path.join(".claude", "CLAUDE.md")):
            f = os.path.join(cur, name)
            if os.path.isfile(f):
                seeds.append(f)
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    glob_md = os.path.join(HOME, ".claude", "CLAUDE.md")
    seeds.append(glob_md)
    found = []
    for s in seeds:
        for t in imports_of(s) + (paths_in(s) if s == glob_md else []):
            v = vault_root(os.path.realpath(t)) if os.path.exists(t) else None
            if v and v not in found:
                found.append(v)
    v = os.path.join(HOME, "vault")
    if os.path.isdir(v):
        v = os.path.realpath(v)
        if os.path.isdir(os.path.join(v, "_Meta")) and v not in found:
            found.append(v)
    return found


def frontmatter(path):
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            head = fh.read(6000)
    except OSError:
        return None
    if not head.startswith("---"):
        return None
    lines = head.split("\n")
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return None
    fm = {}
    for ln in lines[1:end]:
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*?)\s*$", ln)
        if m:
            fm[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return fm


def project_sheets(vault):
    root = os.path.join(vault, "10-Projects")
    if not os.path.isdir(root):
        return []
    out = []
    for r, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if not x.startswith(".")]
        for fn in files:
            if fn.endswith(".md"):
                p = os.path.join(r, fn)
                fm = frontmatter(p)
                if fm and fm.get("type") == "project":
                    out.append((p, fm))
    return out


def under(path, root):
    root = root.rstrip(os.sep)
    return path == root or path.startswith(root + os.sep)


def resolve(d):
    d = os.path.realpath(os.path.abspath(os.path.expanduser(d or os.getcwd())))
    res = {"mode": "none", "vault": "", "sheet": "", "repo": "", "subpath": "", "match": ""}
    v = vault_root(d)
    if v:
        res.update(mode="vault", vault=v)
        return res
    top = git("rev-parse", "--show-toplevel", cwd=d)
    if not top:
        return res
    top = os.path.realpath(top)
    remote = git("remote", "get-url", "origin", cwd=top)
    key = repo_key(remote)
    sub = os.path.relpath(d, top).replace(os.sep, "/")
    sub = "" if sub == "." else sub
    res.update(repo=remote, subpath=sub)

    for vault in candidate_vaults(d):
        best = None  # (rang, -spécificité, chemin)
        for p, fm in project_sheets(vault):
            # 1. repo
            val = fm.get("repo", "")
            if key and val:
                url, _, frag = val.partition("#")
                frag = frag.strip("/")
                if repo_key(url) == key and (not frag or sub == frag or sub.startswith(frag + "/")):
                    cand = (1, -len(frag), p, "repo")
                    if best is None or cand[:2] < best[:2]:
                        best = cand
                    continue
            # 2. dossier-travail (le dossier ou un ancêtre, jusqu'à la racine du dépôt)
            dt = fm.get("dossier-travail", "")
            if dt and not dt.startswith("{"):
                dt = os.path.realpath(os.path.expanduser(dt))
                if under(d, dt) and under(dt, top):
                    cand = (2, -len(dt), p, "dossier-travail")
                    if best is None or cand[:2] < best[:2]:
                        best = cand
                    continue
            # 3. slug
            slug = os.path.basename(p)[:-3]
            if slug in (os.path.basename(d), os.path.basename(top)):
                cand = (3, 0 if slug == os.path.basename(d) else 1, p, "slug")
                if best is None or cand[:2] < best[:2]:
                    best = cand
        if best:
            res.update(mode="repo", vault=vault, sheet=best[2], match=best[3])
            return res
    return res


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--shell"]
    r = resolve(args[0] if args else None)
    if "--shell" in sys.argv:
        for k in ("mode", "vault", "sheet", "repo", "subpath", "match"):
            print(f"{k.upper()}={shlex.quote(r[k])}")
    else:
        print(json.dumps(r, ensure_ascii=False))
