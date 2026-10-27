#!/usr/bin/env python3
"""vault-memory.py — état de la mémoire native de Claude Code, en lecture seule (sauf la sauvegarde, hors vault).

Le script établit les faits ; `sync-vault` et `audit-vault` tranchent. Il n'écrit jamais dans un dossier mémoire ni
dans le vault. Un constat sensible se rend en fichier, ligne et type, jamais en contenu ; un pointeur est rendu
tel qu'écrit, sauf s'il est reconnu comme sensible, auquel cas il est masqué (la détection est heuristique).

  vault-memory.py where [DOSSIER_DE_TRAVAIL]              → dossier mémoire d'un dossier de travail, et sa source
  vault-memory.py inventory [--vault V]                   → JSON : dossiers mémoire de la machine, part du plafond,
                                                            règles répétées d'un dossier à l'autre
  vault-memory.py check [--vault V] [--summary] [DOSSIER] → JSON (ou une ligne) : budget, plafond, index, pointeurs
                                                            vers le vault, sensible apparent, quasi-doublons,
                                                            curation due ; `needs_curation` les résume
  vault-memory.py backup [DOSSIER]                        → copie dans ${XDG_STATE_HOME:-~/.local/state}/
                                                            second-cerveau/memoire/{horodatage}-{empreinte}/

Sans DOSSIER, `check` et `backup` visent le dossier mémoire du dossier courant.

Faits Claude Code (2.1.311, vérifiés dans le binaire le 2026-10-27) :
  - dossier par défaut : `{CLAUDE_CONFIG_DIR ou ~/.claude}/projects/{racine de la copie de travail assainie}/memory/`,
    assainissement : chaque unité UTF-16 hors [a-zA-Z0-9] devient `-`, au-delà de 200 caractères troncature et
    empreinte (fonctions `hL` et `kme`) ; la racine est celle de la copie de travail git principale ;
  - `autoMemoryDirectory` : première source qui le définit parmi policy, flag, puis, si le dossier est de
    confiance, `.claude/settings.local.json` de la racine git (et celui du dossier de lancement) et
    `.claude/settings.json` du seul dossier de lancement, puis les réglages utilisateur. Une valeur ni absolue ni
    en `~/` est rejetée : le dossier par défaut s'applique. Le script ne lit ni policy ni flag, et suppose le
    dossier de confiance ;
  - `MEMORY.md` est chargé après `trim()`, tronqué à 200 lignes et 25 000 caractères (unités UTF-16).

Réglages, dans `{vault}/_Meta/hooks.conf` : MEMORY_MAX_LINES (120) et MEMORY_MAX_KB (16, en milliers de caractères),
budget de l'index ; MEMORY_CURATION_DAYS (30), délai au-delà duquel une curation complète est due (la dernière
sauvegarde du dossier fait foi). Dépendances : python3 (+ git pour trouver la racine d'une copie de travail).
"""
import sys
sys.dont_write_bytecode = True                             # lecture seule : pas de __pycache__ dans le plugin
import datetime as dt, hashlib, importlib.util, json, os, re, shutil, subprocess, tempfile, unicodedata
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


_vr = _load("vault_resolve", "vault-resolve.py")
_vj = _load("vault_journal", "vault-journal.py")
vault_root, conf, conf_int = _vr.vault_root, _vj.conf, _vj.conf_int

HARD_LINES, HARD_CHARS = 200, 25000
ALERT_LINES, ALERT_CHARS = 150, 20000
PARA = ("00-Inbox", "10-Projects", "20-Areas", "30-Resources", "40-Archive", "_Meta", "_personas")
WIKI_RE = re.compile(r"(!?)\[\[([^\[\]\n|#]{1,150}?)(#[^\[\]\n|]*)?(?:\\?\|[^\[\]\n]*)?\]\]")
INDEX_LINK_RE = re.compile(r"\]\(\s*<?([^)<>\n]+?)>?(?:\s+\"[^\"\n]*\")?\s*\)")
BACKUP_RE = re.compile(r"^(\d{8}-\d{6}-\d{6})-([0-9a-f]{12})$")
STOP = set("""avec dans pour plus sans sont cette tout tous elle elles leur leurs être avoir fait faire comme mais
donc quand alors aussi encore toujours jamais rien chaque entre depuis après avant sous vers chez that this with
from have when your then they them what which will would should could there their about into only also just""".split())

# ── sensible ─────────────────────────────────────────────────────────────────────────────────────────────────

TOKEN_RES = [re.compile(p) for p in (
    r"\b(?:sk-ant-|sk-proj-|sk-)[A-Za-z0-9_-]{20,}",
    r"\b(?:sk|rk|pk)_(?:live|test)_[A-Za-z0-9]{10,}",
    r"\bglpat-[A-Za-z0-9_-]{20,}", r"\bgh[opsur]_[A-Za-z0-9]{20,}", r"\bgithub_pat_\w{20,}",
    r"\bntn_[A-Za-z0-9]{20,}", r"\bsecret_[A-Za-z0-9]{30,}", r"\bpat[A-Za-z0-9]{14}\.[a-f0-9]{30,}",
    r"\bxox[abprs]-[\w-]{10,}", r"hooks\.slack\.com/services/T[A-Za-z0-9]+/B[A-Za-z0-9]+/[A-Za-z0-9]+",
    r"\bAKIA[0-9A-Z]{16}\b", r"\bAIza[0-9A-Za-z_-]{30,}", r"\bxkeysib-[a-f0-9]{40,}",
    r"\beyJ[\w-]{10,}\.[\w-]{10,}\.[\w-]{10,}", r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    r"\b[a-z][a-z0-9+.-]{0,30}://[^\s/:@]{1,100}:[^\s/@]{3,100}@",
    r"\bBearer\s+(?![$<{])[A-Za-z0-9._~+/=-]{16,}",
)]
KEYWORD_RE = re.compile(r"(?i)(?<![A-Za-z])(api[_ -]?key|access[_ -]?key|secret(?:[_ -]?(?:access[_ -]?)?key)?|"
                        r"client[_ -]?secret|token|password|passwd|pwd|mdp|mot de passe)\b[^\n:=/`]{0,30}?[:=]\s*"
                        r"[`'\"]?([^\s`'\",;]{8,})")
IBAN_RE = re.compile(r"(?ai)\b([a-z]{2}\d{2}(?:[ -]?[a-z0-9]{4}){3,7}(?:[ -]?[a-z0-9]{1,3})?)\b")
PHONE_RE = re.compile(r"(?<![\w.:/-])(?:(?:\+|00)33\s?(?:\(0\)\s?)?|0)[1-9]([\s.-]?)\d{2}(?:\1\d{2}){3}(?![\w.:/-])"
                      r"|(?<![\w.:/-])\+(?!33)\d{1,3}[\s.-]?(?:\(\d{1,4}\)[\s.-]?)?\d{2,4}(?:[\s.-]?\d{2,4}){2,4}(?![\w.:/-])")
NOT_PHONE_CONTEXT = re.compile(r"(?i)(?<!\w)(commande|order|n°|no\.|ticket|facture|réf|ref|siret|siren|id)\W{0,3}$")


def iban_valid(raw):
    s = re.sub(r"[ -]", "", raw).upper()
    if not 15 <= len(s) <= 34 or not s.isascii() or not s.isalnum():
        return False
    try:
        return int("".join(str(int(c, 36)) for c in s[4:] + s[:4])) % 97 == 1
    except ValueError:
        return False


CODE_PREFIXES = ("input.", "process.", "os.environ", "env.", "config.", "settings.", "this.", "self.",
                 "secrets.", "vars.", "args.", "params.", "req.", "request.")


FILE_LIKE = re.compile(r"^[\w.-]+\.(md|txt|json|env|ya?ml|toml|ini|sh|py|js|ts|html|csv|pdf|docx?|xlsx?)$", re.I)


def keyword_value_is_secret(val):
    """Une valeur littérale plausible : ni variable, substitution, chemin, URL, expression de code, nom de fichier,
    nom de variable en capitales, valeur tronquée ou simple mot ; au moins un chiffre ou un symbole, et deux
    classes de caractères."""
    if any(x in val for x in ("…", "...", "xxx", "XXX", "<", "{", "(", "://", "=")) or val[0] in "$(/~":
        return False
    if val.lower().startswith(CODE_PREFIXES) or FILE_LIKE.match(val) or re.fullmatch(r"[A-Z][A-Z0-9_]+", val):
        return False
    if val.isdigit() or re.fullmatch(r"[^\W\d_]+[.!?]?", val):  # compte de tokens, mot ordinaire
        return False
    classes = sum(bool(re.search(p, val)) for p in (r"[a-z]", r"[A-Z]", r"\d", r"[^\w]|_"))
    return classes >= 2 and bool(re.search(r"\d|[^\w]|_", val))


def sensitive_kinds(line, slug_re=None):
    kinds = []
    if any(r.search(line) for r in TOKEN_RES):
        kinds.append("secret")
    if any(keyword_value_is_secret(m.group(2)) for m in KEYWORD_RE.finditer(line)):
        kinds.append("secret")
    if any(iban_valid(m.group(1)) for m in IBAN_RE.finditer(line)):
        kinds.append("iban")
    for m in PHONE_RE.finditer(line):
        if not NOT_PHONE_CONTEXT.search(line[max(0, m.start() - 20):m.start()]):
            kinds.append("téléphone"); break
    if slug_re and slug_re.search(line):
        kinds.append("fiche confidentielle citée")
    return sorted(set(kinds))


def redact(s):
    return "[masqué]" if sensitive_kinds(s) else s


# ── emplacement ──────────────────────────────────────────────────────────────────────────────────────────────

def config_dir():
    v = (os.environ.get("CLAUDE_CONFIG_DIR") or "").strip()
    return os.path.realpath(os.path.expanduser(v)) if v else os.path.join(os.path.expanduser("~"), ".claude")


def _units(s):
    b = s.encode("utf-16-le", "surrogatepass")
    return [int.from_bytes(b[i:i + 2], "little") for i in range(0, len(b), 2)]


def _kme(s):
    """Empreinte de Claude Code (`kme`) : hash 31 sur les unités UTF-16, entier signé 32 bits."""
    h = 0
    for u in _units(s):
        h = (h * 31 + u) & 0xFFFFFFFF
    return h - (1 << 32) if h & 0x80000000 else h


def _base36(n):
    chars, out = "0123456789abcdefghijklmnopqrstuvwxyz", ""
    while True:
        n, r = divmod(n, 36); out = chars[r] + out
        if not n:
            return out


def sanitize(path):
    """Port de `hL` : unités UTF-16 hors [a-zA-Z0-9] remplacées par `-`, troncature à 200 avec empreinte."""
    s = "".join(chr(u) if u < 128 and chr(u).isalnum() else "-" for u in _units(path))
    return s if len(s) <= 200 else f"{s[:200]}-{_base36(abs(_kme(path)))}"


def git_root(d):
    """Racine de la copie de travail principale : celle du dépôt pour un worktree lié, sinon --show-toplevel."""
    def run(*a):
        try:
            r = subprocess.run(["git", *a], cwd=d, capture_output=True, text=True, timeout=5)
            return r.stdout.strip() if r.returncode == 0 else ""
        except Exception:
            return ""
    common = run("rev-parse", "--path-format=absolute", "--git-common-dir")
    if common and os.path.basename(common.rstrip("/")) == ".git":
        return os.path.realpath(os.path.dirname(common.rstrip("/")))
    top = run("rev-parse", "--show-toplevel")
    return os.path.realpath(top) if top else None


def read_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def configured_dir(workdir, root=None):
    """`autoMemoryDirectory` : première source qui définit la clé, dans l'ordre de Claude Code : settings.local.json
    de la racine git, puis celui du dossier de lancement, settings.json du dossier de lancement seul, puis réglages
    utilisateur. Rend (dossier ou None, source). Une valeur invalide (ni absolue ni en `~/`, espaces compris) arrête
    la recherche : Claude Code prend alors le dossier par défaut."""
    root = root or workdir
    sources = [("local", os.path.join(root, ".claude", "settings.local.json"))]
    if workdir != root:                                    # settings.local.json « legacy » du dossier de lancement
        sources.append(("local", os.path.join(workdir, ".claude", "settings.local.json")))
    sources += [("projet", os.path.join(workdir, ".claude", "settings.json")),   # dossier de lancement seulement
                ("utilisateur", os.path.join(config_dir(), "settings.json"))]
    for src, path in sources:
        data = read_json(path)
        if "autoMemoryDirectory" not in data:
            continue
        val = data["autoMemoryDirectory"]
        if isinstance(val, str) and (os.path.isabs(val) or val.startswith("~/")):
            return os.path.realpath(os.path.expanduser(val)), src
        return None, f"{src} (valeur rejetée)"
    return None, None


def memory_dir(workdir):
    workdir = os.path.realpath(os.path.expanduser(workdir))
    root = git_root(workdir) or workdir
    cfg, src = configured_dir(workdir, root)
    if cfg:
        return cfg, src
    default = os.path.join(config_dir(), "projects", sanitize(root), "memory")
    return default, "défaut" + (f", {src}" if src else "")


# ── lecture ──────────────────────────────────────────────────────────────────────────────────────────────────

def read_text(path):
    with open(path, "rb") as fh:
        return fh.read().decode("utf-8", errors="replace")


def display(name):
    """Nom de fichier affichable : un nom non UTF-8 (octets échappés par le système) est rendu avec �."""
    return name.encode("utf-8", "surrogateescape").decode("utf-8", "replace")


def memory_files(d):
    """Fichiers mémoire lisibles, et la liste des illisibles."""
    out, unreadable = [], []
    try:
        names = sorted(os.listdir(d))
    except OSError:
        return [], ["(dossier illisible)"]
    for fn in names:
        p = os.path.join(d, fn)
        if not fn.endswith(".md") or fn == "MEMORY.md" or not os.path.isfile(p):
            continue
        try:
            text = read_text(p)
            mtime = os.path.getmtime(p)
        except OSError:
            unreadable.append(display(fn)); continue
        head = text.split("\n---", 1)[0] if text.startswith("---") else ""
        m = re.search(r"(?m)^\s*type:\s*([\w-]+)", head)
        out.append({"file": display(fn), "text": text, "type": m.group(1) if m else "", "mtime": mtime})
    return out, unreadable


def index_stats(d):
    p = os.path.join(d, "MEMORY.md")
    try:
        raw = read_text(p) if os.path.isfile(p) else ""
    except OSError:
        raw = ""
    text = raw.strip()                                     # Claude Code compte après trim()
    links = []
    for target in INDEX_LINK_RE.findall(text):
        target = target.split("#", 1)[0].strip().replace("%20", " ")
        target = os.path.normpath(target) if target else target
        if target and "/" not in target and not target.startswith("~") and target.endswith(".md"):
            links.append(target)                           # un lien vers le vault n'est pas une entrée d'index
    return {"raw": raw, "lines": text.count("\n") + 1 if text else 0, "chars": len(_units(text)), "links": links}


def dir_summary(d, project=""):
    files, unreadable = memory_files(d)
    idx = index_stats(d)
    return {"dir": d, "project": project, "files": len(files), "unreadable": unreadable,
            "index_lines": idx["lines"], "index_chars": idx["chars"],
            "cap_pct": round(100 * max(idx["lines"] / HARD_LINES, idx["chars"] / HARD_CHARS)),
            "types": dict(Counter(f["type"] or "?" for f in files)),
            "newest": dt.date.fromtimestamp(max(f["mtime"] for f in files)).isoformat() if files else None}


def all_dirs(vault=None):
    base = os.path.join(config_dir(), "projects")
    seen, out = set(), []

    def add(d, label):
        real = os.path.realpath(d)
        if os.path.isdir(d) and real not in seen:
            seen.add(real); out.append((d, label))

    try:
        names = sorted(os.listdir(base))
    except OSError:
        names = []
    for name in names:
        add(os.path.join(base, name, "memory"), name)
    for workdir in ([vault] if vault else []) + [os.path.expanduser("~")]:
        cfg, src = configured_dir(workdir, workdir)
        if cfg:
            add(cfg, f"autoMemoryDirectory ({src})")
    return out


# ── pointeurs vers le vault ──────────────────────────────────────────────────────────────────────────────────

PATHS_KEY = "\x00chemins"


def nfc(s):
    return unicodedata.normalize("NFC", s)


def exists_in_vault(rel, vault, names):
    """Existence d'un chemin relatif, y compris quand le fichier est nommé en NFD (vault venu d'un Mac)."""
    rel = rel.rstrip("/")
    if os.path.exists(os.path.join(vault, rel)) or os.path.exists(os.path.join(vault, rel + ".md")):
        return True
    paths = names.get(PATHS_KEY, set())
    return nfc(rel) in paths or nfc(rel + ".md") in paths


def vault_index(vault):
    """{nom en casse repliée (avec et sans extension): [chemins relatifs]} et l'expression des fiches sensibles."""
    names, sensitive, paths = {}, set(), set()
    for r, dirs, files in os.walk(vault):
        dirs[:] = [x for x in dirs if not x.startswith(".")]
        rel_dir = os.path.relpath(r, vault).replace(os.sep, "/")
        for fn in files:
            rel = (rel_dir + "/" + fn) if rel_dir != "." else fn
            paths.add(nfc(rel))
            for k in range(1, rel.count("/") + 1):         # dossiers aussi
                paths.add(nfc(rel.rsplit("/", k)[0]))
            key = unicodedata.normalize("NFC", fn).casefold()
            names.setdefault(key, []).append(rel)
            if fn.endswith(".md"):
                names.setdefault(key[:-3], []).append(rel)
            else:
                continue
            slug = fn[:-3]
            if "🔒" in rel:
                sensitive.add(slug); continue
            try:
                with open(os.path.join(r, fn), encoding="utf-8", errors="ignore") as fh:
                    head = fh.read(3000)
            except OSError:
                continue
            fm = head.split("\n---", 1)[0] if head.startswith("---") else ""
            title = next((ln for ln in head.splitlines() if ln.startswith("# ")), "")
            if "🔒" in title or re.search(r"(?mi)^(sensibilit[ée]:\s*[\"']?confidentiel|confidentiel:\s*[\"']?(true|oui|1))", fm):
                sensitive.add(slug)
    parts = []
    for slug in sorted(sensitive, key=len, reverse=True):
        if len(slug) < 4:
            continue
        parts.append(r"\[\[" + re.escape(slug) + r"(?=[\]|#])")       # wikilink : toujours
        if "-" in slug and len(slug) >= 6:                             # nom composé : aussi en clair
            parts.append(r"(?<![\w-])" + re.escape(slug) + r"(?![\w-])")
    slug_re = re.compile("|".join(parts), re.I) if parts else None
    names[PATHS_KEY] = paths
    return names, slug_re


def path_re(vault):
    """Chemins PARA, nus ou préfixés par le vault (chemin réel, `~/…`, ou le lien `~/vault`)."""
    home = os.path.expanduser("~")
    prefixes = {vault, os.path.realpath(vault)}
    alias = os.path.join(home, "vault")
    if os.path.realpath(alias) == os.path.realpath(vault):
        prefixes.add(alias)
    prefixes |= {"~" + p[len(home):] for p in list(prefixes) if p.startswith(home + "/")}
    pre = "|".join(re.escape(p.rstrip("/") + "/") for p in sorted(prefixes, key=len, reverse=True))
    return re.compile(r"(?:(?:" + pre + r")|(?<![\w./-]))((?:" + "|".join(map(re.escape, PARA)) +
                      r")/[^\s`'\"()<>\[\]|,;]{1,200})")


def resolve_name(name, names, vault):
    """Chemins candidats pour un nom de lien, sans casse, avec ou sans extension, ou un chemin relatif au vault."""
    n = unicodedata.normalize("NFC", name.strip()).casefold()
    if "/" in n:
        if exists_in_vault(name.strip(), vault, names):
            return [name.strip()]
        n = n.rsplit("/", 1)[1]
    return names.get(n, [])


def classify(pointer, cands):
    live = [p for p in cands if not p.startswith("40-Archive/")]
    if len(live) == 1:
        return {"kind": "déplacé", "pointer": pointer, "now": live[0]}
    if len(live) > 1:
        return {"kind": "ambigu", "pointer": pointer, "candidates": len(live)}
    if cands:
        return {"kind": "archivé", "pointer": pointer, "now": cands[0]}
    return {"kind": "cassé", "pointer": pointer}


FENCE_BLOCK_RE = re.compile(r"(?ms)^\s*(```|~~~).*?^\s*\1[^\n]*$")
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")


def pointer_findings(text, vault, names, prx, memory_names=()):
    """Pointeurs vers le vault : chemins PARA et [[wikilinks]]. Un lien vers une autre mémoire est valide ; un
    chemin gabarit (`{slug}`, `…`, `AAAA-MM-JJ`) n'est pas un pointeur. Un bloc de code n'en contient pas ; un
    wikilink entre accents graves n'est pas un lien ; un chemin entre accents graves est contrôlé et marqué `code`
    (exemple possible) : cassé ou archivé, il ne compte pas pour `needs_curation` ; déplacé, il compte. Un pointeur reconnu comme sensible est masqué."""
    out = []
    text = FENCE_BLOCK_RE.sub("", text)
    in_code = set()
    for m in INLINE_CODE_RE.finditer(text):
        in_code |= set(prx.findall(m.group(0)))
    wiki_text = INLINE_CODE_RE.sub("", text)
    for raw in prx.findall(text):
        rel = raw.split("#", 1)[0].strip("*").rstrip(".:;!?»*)")    # `_` reste : il ouvre `_Meta`, `_personas`
        if any(c in rel for c in "{}…*<>") or re.search(r"AAAA|YYYY|MM-JJ|MM-DD", rel):
            continue
        if exists_in_vault(rel, vault, names):
            continue
        base = os.path.basename(rel.rstrip("/"))
        cands = [p for p in resolve_name(base, names, vault) if nfc(p) != nfc(rel)]
        finding = classify(redact(rel), cands)
        if raw in in_code:
            finding["code"] = True
        out.append(finding)
    for embed, target, _anchor in WIKI_RE.findall(wiki_text):
        name = target.strip().replace("\\", "")
        if any(c in name for c in "{}…*") or name.casefold() in memory_names:
            continue
        if name.casefold().endswith(".md") and name[:-3].casefold() in memory_names:
            continue
        cands = resolve_name(name[:-3] if name.casefold().endswith(".md") else name, names, vault) or \
            resolve_name(name, names, vault)
        if cands and any(not p.startswith("40-Archive/") for p in cands):
            continue
        out.append(dict(classify(redact(f"{embed}[[{name}]]"), cands), kind="archivé" if cands else "cassé"))
    return out


# ── doublons ─────────────────────────────────────────────────────────────────────────────────────────────────

def tokens(text):
    body = text.split("\n---", 1)[1] if text.startswith("---") and "\n---" in text else text
    return {w for w in re.findall(r"[a-zà-öø-ÿ]{4,}", body.lower()) if w not in STOP}


def near_duplicates(items, threshold):
    out = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i][1], items[j][1]
            s = len(a & b) / len(a | b) if a and b else 0.0
            if s >= threshold:
                out.append({"a": items[i][0], "b": items[j][0], "similarity": round(s, 2)})
    return out


def cross_repeats(dirs, threshold=0.5):
    items = []
    for d, project in dirs:
        for f in memory_files(d)[0]:
            if f["type"] in ("feedback", "user", ""):
                items.append((f"{project}/{f['file']}", tokens(f["text"])))
    return [x for x in near_duplicates(items, threshold) if x["a"].split("/")[0] != x["b"].split("/")[0]]


# ── sauvegarde ───────────────────────────────────────────────────────────────────────────────────────────────

def state_base():
    base = os.environ.get("XDG_STATE_HOME") or os.path.join(os.path.expanduser("~"), ".local", "state")
    return os.path.join(base, "second-cerveau", "memoire")


def fingerprint(d):
    return hashlib.sha256(os.path.realpath(d).encode("utf-8", "surrogatepass")).hexdigest()[:12]


def last_backup(d):
    try:
        names = os.listdir(state_base())
    except OSError:
        return None
    fp = fingerprint(d)
    stamps = [m.group(1) for m in map(BACKUP_RE.match, names) if m and m.group(2) == fp]
    return max(stamps) if stamps else None


def backup(d):
    if not os.path.isdir(d):
        raise SystemExit(f"dossier mémoire introuvable : {d}")
    if os.path.basename(os.path.realpath(d)) != "memory" and not os.path.isfile(os.path.join(d, "MEMORY.md")):
        raise SystemExit(f"{d} n'a pas l'allure d'un dossier mémoire (ni `memory/`, ni MEMORY.md) : refus")
    base = state_base()
    os.makedirs(base, exist_ok=True)
    name = dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f") + "-" + fingerprint(d)
    tmp = tempfile.mkdtemp(dir=base, prefix=".en-cours-")
    try:
        shutil.copytree(d, os.path.join(tmp, "copie"), symlinks=True)
        with open(os.path.join(tmp, "copie", ".source"), "w", encoding="utf-8") as fh:
            fh.write(os.path.realpath(d) + "\n")
        os.rename(os.path.join(tmp, "copie"), os.path.join(base, name))   # visible seulement une fois complète
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return os.path.join(base, name)


# ── contrôle ─────────────────────────────────────────────────────────────────────────────────────────────────

def check(d, vault=None):
    files, unreadable = memory_files(d)
    idx = index_stats(d)
    max_lines = conf_int(vault, "MEMORY_MAX_LINES", 120) if vault else 120
    max_chars = (conf_int(vault, "MEMORY_MAX_KB", 16) if vault else 16) * 1000
    days = conf_int(vault, "MEMORY_CURATION_DAYS", 30) if vault else 30
    res = dir_summary(d)
    res.update(budget_lines=max_lines, budget_chars=max_chars,
               over_budget=idx["lines"] > max_lines or idx["chars"] > max_chars,
               alert=idx["lines"] > ALERT_LINES or idx["chars"] > ALERT_CHARS,
               truncated=idx["lines"] > HARD_LINES or idx["chars"] > HARD_CHARS)
    in_dir = {f["file"] for f in files} | set(u for u in unreadable if not u.startswith("("))
    linked = set(idx["links"])
    res["index"] = {"missing_files": sorted(linked - in_dir), "unindexed": sorted(in_dir - linked)}
    res["pointers"], res["sensitive"] = [], []
    names, slug_re = vault_index(vault) if vault else ({}, None)
    prx = path_re(vault) if vault else None
    mem_names = {f["file"][:-3].casefold() for f in files} | {f["file"][:-3].casefold().replace("_", "-") for f in files}
    for name, text in [("MEMORY.md", idx["raw"])] + [(f["file"], f["text"]) for f in files]:
        if vault:
            for x in pointer_findings(text, vault, names, prx, mem_names):
                res["pointers"].append(dict(file=name, **x))
        for no, line in enumerate(text.split("\n"), 1):
            for kind in sensitive_kinds(line, slug_re):
                res["sensitive"].append({"file": name, "line": no, "kind": kind})
    res["duplicates"] = near_duplicates([(f["file"], tokens(f["text"])) for f in files], 0.6)
    lb = last_backup(d)
    res["last_backup"] = lb
    age = (dt.datetime.now() - dt.datetime.strptime(lb[:15], "%Y%m%d-%H%M%S")).days if lb else None
    res["curation_due"] = bool(files) and (lb is None or age >= days)
    res["needs_curation"] = bool(res["over_budget"] or res["sensitive"] or res["duplicates"] or res["curation_due"]
                                 or [p for p in res["pointers"] if p["kind"] != "ambigu"
                                     and not (p.get("code") and p["kind"] in ("cassé", "archivé"))]
                                 or res["index"]["missing_files"] or res["index"]["unindexed"])
    return res


def summary_line(r):
    segs = []
    if r["truncated"]:
        segs.append(f"index tronqué au chargement ({r['index_lines']} lignes, {r['index_chars']} caractères ; "
                    f"plafond {HARD_LINES} lignes, {HARD_CHARS} caractères)")
    elif r["over_budget"]:
        segs.append(f"index de {r['index_lines']} lignes et {r['index_chars']} caractères, au-dessus du budget de "
                    f"{r['budget_lines']} lignes et {r['budget_chars']} caractères")
    if r["sensitive"]:
        segs.append(f"{len({x['file'] for x in r['sensitive']})} mémoire(s) au contenu sensible apparent")
    if r.get("unreadable"):
        segs.append(f"{len(r['unreadable'])} fichier(s) ou dossier mémoire illisible(s)")
    return ("Mémoire native : " + ", ".join(segs) + " ; curation par sync-vault") if segs else ""


# ── interface ────────────────────────────────────────────────────────────────────────────────────────────────

def main(argv):
    if not argv or argv[0] not in ("inventory", "check", "backup", "where"):
        print(__doc__); return 2
    cmd, args = argv[0], argv[1:]

    def opt(name):
        if name in args:
            i = args.index(name)
            if i + 1 >= len(args):
                raise SystemExit(f"{name} attend une valeur")
            v = args[i + 1]; del args[i:i + 2]; return v
        return None

    def flag(name):
        if name in args:
            args.remove(name); return True
        return False

    vault = opt("--vault")
    vault = os.path.realpath(vault) if vault else vault_root(os.getcwd())
    summary = flag("--summary")
    if cmd == "where":
        d, src = memory_dir(args[0] if args else os.getcwd())
        print(json.dumps({"dir": d, "source": src, "exists": os.path.isdir(d)}, ensure_ascii=False))
        return 0
    if cmd == "inventory":
        dirs = all_dirs(vault)
        out = {"hard_cap": {"lines": HARD_LINES, "chars": HARD_CHARS},
               "dirs": sorted((dir_summary(d, p) for d, p in dirs), key=lambda x: -x["cap_pct"]),
               "cross_repeats": cross_repeats(dirs)}
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 0
    target = args[0] if args else memory_dir(os.getcwd())[0]
    if cmd == "backup":
        print(json.dumps({"backup": backup(target)}, ensure_ascii=False))
        return 0
    if not os.path.isdir(target):
        if not summary:
            print(json.dumps({"dir": target, "files": 0}, ensure_ascii=False))
        return 0
    if summary:
        try:
            line = summary_line(check(target, vault))
        except Exception as e:                             # le bilan de démarrage ne devient jamais muet
            line = f"Mémoire native : contrôle en échec ({e.__class__.__name__}), lancer vault-memory.py check"
        if line:
            print(line)
        return 0
    r = check(target, vault)
    print(json.dumps(r, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
