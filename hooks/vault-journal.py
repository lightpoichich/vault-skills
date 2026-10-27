#!/usr/bin/env python3
"""vault-journal.py — rotation des journaux de fiche, mot pour mot, sans LLM.

Une fiche tient son état courant dans ses sections ordinaires et ses entrées datées dans une section de journal
(`## Journal` par défaut). Quand la fiche dépasse son budget de taille, les entrées les plus anciennes sortent,
à l'identique, vers `{dossier de la fiche}/journal/{slug}-{AAAA}-T{n}.md`. La fiche garde un index `## Journaux`.

  vault-journal.py check  [--vault V] [--summary]       → JSON (ou une ligne) : fiches au-dessus du budget
  vault-journal.py rotate [--apply] [--force] FICHE…    → simulation par défaut ; --apply écrit
  vault-journal.py rotate [--apply] [--force] --all [--vault V]
  vault-journal.py verify [--loose] --before A… --after B…   → 0 si aucune ligne de A ne manque dans B

Réglages, dans `{vault}/_Meta/hooks.conf` (absents : valeurs entre parenthèses) :
  JOURNAL_ROTATION=1          autorise `rotate --apply` sans --force (0 : rotation coupée)
  JOURNAL_MAX_KB_{TYPE}=Ko    budget par type de fiche (AREA=20, PROJECT=30 ; tiret du type → _)
  JOURNAL_MAX_KB=30           budget des autres types, appliqué seulement aux fiches qui ont une section de journal
  JOURNAL_SECTIONS=Journal    sections rotables (liste blanche, séparée par des virgules) ; tout le reste est protégé
  JOURNAL_KEEP=5              entrées datées les plus récentes jamais déplacées, par section

Règles (rien ne bouge en cas de doute) :
  - entrée = puce de premier niveau avec ses lignes indentées, ou bloc `###` ; blocs de code opaques (clôture
    CommonMark : même caractère, longueur au moins égale) ;
  - fiche bloquée entière si un bloc de code reste ouvert, ou si un bloc ouvert en retrait déborde de son entrée
    (ligne non vide moins indentée que l'ouverture) ;
  - section bloquée si elle mêle puces et `###` (puce datée sous un `###`, ou `###` après des puces), ou si un
    paragraphe ou un bloc de code s'intercale entre deux entrées en colonne 0 ;
  - date d'une entrée : celle qui ouvre sa ligne de tête (après la puce, la case à cocher et le gras éventuels),
    au format AAAA-MM-JJ ou JJ/MM/AAAA. Une entrée sans cette date, y compris une date sans année, ou dont la date
    est à plus d'un an de ses deux voisines datées (faute de frappe probable), reste épinglée dans la fiche et se
    signale ; elle ne bloque pas les autres ;
  - on sort les entrées datées les plus anciennes jusqu'à 80 % du budget, jamais les JOURNAL_KEEP plus récentes ;
    elles s'ajoutent au journal du trimestre dans l'ordre de la rotation ;
  - avant écriture : non-perte vérifiée, sauvegarde hors vault (${XDG_STATE_HOME:-~/.local/state}/second-cerveau/
    rotation/), octets de la fiche et des journaux comparés à la lecture, avant le commit git puis après le fsync
    du temporaire, juste avant chaque remplacement ; écriture atomique, destinations d'abord, droits conservés ; dans
    un vault git, commit des seuls chemins touchés, avant (s'ils étaient modifiés) et après.
Dépendances : python3 (+ git si le vault en est un).
"""
import sys
sys.dont_write_bytecode = True                             # pas de __pycache__ dans le dossier du plugin
import datetime as dt, importlib.util, json, os, re, shutil, stat, subprocess, tempfile, unicodedata
from collections import Counter

_spec = importlib.util.spec_from_file_location("vault_resolve", os.path.join(os.path.dirname(os.path.abspath(__file__)), "vault-resolve.py"))
_vr = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_vr)
vault_root, unquote = _vr.vault_root, _vr.unquote

DEFAULT_BUDGETS = {"AREA": 20, "PROJECT": 30}
SKIP_DIRS = ("_Meta/", "_personas/", ".obsidian/", ".claude/", ".git/", ".trash/", "40-Archive/", "00-Inbox/")
TARGET = 0.8

BULLET_RE = re.compile(r"^([-*+]|\d+[.)])\s")
H3_RE = re.compile(r"^###\s")
H12_RE = re.compile(r"^#{1,2}\s")
FENCE_OPEN_RE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
HEAD_RE = re.compile(r"^(?:\s*(?:[-*+]|\d+[.)])\s+(?:\[[ xX]\]\s+)?|###\s+)(?:\*\*|__|\*|_)?\s*(?:\[\[)?"
                     r"(?:(\d{4})-(\d{2})-(\d{2})|(\d{1,2})/(\d{1,2})/(\d{4}))(?!\d)")
REL_LINK_RE = re.compile(r"\]\((?!https?:|mailto:|#|/|obsidian:)([^)\s]+)\)")


# ── configuration ────────────────────────────────────────────────────────────────────────────────────────────

def conf_lines(vault):
    try:
        with open(os.path.join(vault, "_Meta", "hooks.conf"), encoding="utf-8", errors="ignore") as fh:
            return fh.read().splitlines()
    except OSError:
        return []


def conf(vault, key, default):
    """Même lecture que `vault_conf` de vault-lib.sh : dernière occurrence, commentaire de fin retiré."""
    val = None
    for ln in conf_lines(vault):
        m = re.match(r"^\s*" + re.escape(key) + r"\s*=\s*(.*)$", ln)
        if m:
            val = re.sub(r"\s*#.*$", "", m.group(1)).strip()
    return val if val else default


def conf_int(vault, key, default):
    try:
        return max(0, int(conf(vault, key, str(default))))
    except ValueError:
        return default


def settings(vault):
    s = {
        "rotation": conf(vault, "JOURNAL_ROTATION", "0") in ("1", "on", "true", "oui", "yes"),
        "sections": [x.strip().casefold() for x in conf(vault, "JOURNAL_SECTIONS", "Journal").split(",") if x.strip()],
        "keep": conf_int(vault, "JOURNAL_KEEP", 5),
        "default_kb": conf_int(vault, "JOURNAL_MAX_KB", 30) or 30,
        "budgets": dict(DEFAULT_BUDGETS),
        "exclude": [e.strip().strip("/") + "/" for e in conf(vault, "EXCLUDE", "").split(",") if e.strip()],
    }
    for ln in conf_lines(vault):
        m = re.match(r"^\s*JOURNAL_MAX_KB_([A-Z0-9_]+)\s*=\s*(\d+)", ln)
        if m and int(m.group(2)) > 0:
            s["budgets"][m.group(1)] = int(m.group(2))
    return s


def budget_kb(s, ftype, has_journal):
    key = (ftype or "").upper().replace("-", "_")
    if key in s["budgets"]:
        return s["budgets"][key]
    return s["default_kb"] if has_journal else None


# ── lecture d'une fiche ──────────────────────────────────────────────────────────────────────────────────────

def fences(lines, start=0):
    """Pour chaque ligne : (dans un bloc de code ?, ligne d'ouverture ?). Rend aussi le bloc resté ouvert et la
    première ligne d'un bloc ouvert en retrait qui déborde de son entrée (ligne non vide moins indentée que
    l'ouverture : en CommonMark, le bloc s'est fermé avec l'item)."""
    flags, opener, broken = [], None, None
    for i, raw in enumerate(lines):
        ln = raw.rstrip("\r")
        if i < start:
            flags.append((False, False)); continue
        if opener is None:
            m = FENCE_OPEN_RE.match(ln)
            if m and not (m.group(2)[0] == "`" and "`" in m.group(3)):
                opener = (m.group(2)[0], len(m.group(2)), i, len(m.group(1)))
                flags.append((True, True)); continue
            flags.append((False, False))
        else:
            ch, n, _, indent = opener
            if ln.strip() and len(ln) - len(ln.lstrip()) < indent and broken is None:
                broken = i
            if re.match(r"^\s*" + re.escape(ch) + "{" + str(n) + r",}\s*$", ln):
                opener = None
            flags.append((True, False))
    return flags, opener, broken


class Note:
    """Fiche découpée en lignes. Les fins de ligne sont gardées telles quelles : '\\n'.join(lines) == texte."""

    def __init__(self, path):
        self.path = path
        with open(path, "rb") as fh:
            self.mode = stat.S_IMODE(os.fstat(fh.fileno()).st_mode)
            self.raw = fh.read()
        self.text = self.raw.decode("utf-8")
        self.lines = self.text.split("\n")
        self.nl = "\r\n" if self.text.count("\r\n") * 2 > self.text.count("\n") else "\n"   # fin de ligne majoritaire
        self.fm, self.body_start = {}, 0
        if self.lines and self.lines[0].lstrip("﻿").rstrip("\r") == "---":
            end = next((i for i in range(1, len(self.lines)) if self.lines[i].rstrip("\r") == "---"), None)
            if end is not None:
                self.body_start = end + 1
                for ln in self.lines[1:end]:
                    m = re.match(r"^([^\s:#][^\s:]*):\s*(.*?)\s*$", ln.rstrip("\r"))
                    if m:
                        self.fm[unicodedata.normalize("NFC", m.group(1))] = unquote(m.group(2))
        flags, opener, broken = fences(self.lines, self.body_start)
        self.fence = [f for f, _ in flags]
        self.fence_open = [o for _, o in flags]
        self.blocked = None
        if opener:
            self.blocked = f"ligne {opener[2] + 1} : bloc de code jamais refermé"
        elif broken is not None:
            self.blocked = f"ligne {broken + 1} : bloc de code qui déborde de son entrée"

    def line(self, i):
        return self.lines[i].rstrip("\r")

    def sections(self):
        """[(titre, i_titre, i_fin)] des sections `##` (fin exclue), hors blocs de code."""
        heads = [i for i in range(self.body_start, len(self.lines)) if not self.fence[i] and H12_RE.match(self.line(i))]
        out = []
        for k, i in enumerate(heads):
            if self.line(i).startswith("## "):
                end = heads[k + 1] if k + 1 < len(heads) else len(self.lines)
                out.append((self.line(i)[3:].strip(), i, end))
        return out

    def same_on_disk(self):
        try:
            with open(self.path, "rb") as fh:
                return fh.read() == self.raw
        except OSError:
            return False


def head_date(line):
    """Date qui ouvre la ligne de tête d'une entrée (AAAA-MM-JJ ou JJ/MM/AAAA), None sinon."""
    m = HEAD_RE.match(line)
    if not m:
        return None
    if m.group(1):
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    else:
        d, mo, y = int(m.group(4)), int(m.group(5)), int(m.group(6))
    if not 1970 <= y <= 2100:
        return None
    try:
        return dt.date(y, mo, d)
    except ValueError:
        return None


class Section:
    """Section rotable analysée : entrées [début, fin_contenu, date|None], ordre, blocage éventuel."""

    def __init__(self, note, title, start, end):
        self.note, self.title, self.start, self.end = note, title, start, end
        self.units, self.blocked, self.order, self.undated = [], None, "recent-first", []
        self._split()
        if not self.blocked:
            self._date()

    def _split(self):
        n, kind, cur = self.note, None, None
        for i in range(self.start + 1, self.end):
            ln = n.line(i)
            if n.fence_open[i] and ln[:1] not in (" ", "\t") and kind == "bullet" and cur is not None:
                self.blocked = f"ligne {i + 1} : bloc de code en colonne 0 entre deux entrées"; return
            if n.fence[i] or not ln.strip() or ln[:1] in (" ", "\t"):
                if cur is not None and ln.strip():
                    cur[1] = i + 1
                continue
            is_bullet, is_h3 = bool(BULLET_RE.match(ln)), bool(H3_RE.match(ln))
            if is_h3 and kind == "bullet":
                self.blocked = f"ligne {i + 1} : titre ### après des entrées en puces"; return
            if is_bullet and kind == "h3" and head_date(ln):
                self.blocked = f"ligne {i + 1} : puce datée sous un titre ###"; return
            if is_h3 or (is_bullet and kind != "h3"):
                kind, cur = ("h3" if is_h3 else "bullet"), [i, i + 1]
                self.units.append(cur)
            elif cur is None:
                continue                                  # introduction avant la première entrée : reste en place
            elif kind == "h3":
                cur[1] = i + 1                            # paragraphe ou puce sans date dans un bloc ###
            else:
                self.blocked = f"ligne {i + 1} : paragraphe intercalé entre deux entrées"; return

    def _date(self):
        """Date de chaque entrée ; une entrée sans date en tête reste épinglée (None) et ne bloque pas les autres."""
        dates = [head_date(self.note.line(u[0])) for u in self.units]
        idx = [k for k, d in enumerate(dates) if d]
        isolated = set()
        for pos, k in enumerate(idx):                      # faute de frappe probable (2016 pour 2026) : épinglée
            near = [dates[idx[q]] for q in (pos - 1, pos + 1) if 0 <= q < len(idx)]
            if near and all(abs((dates[k] - x).days) > 366 for x in near):
                isolated.add(k)
        dates = [None if k in isolated else d for k, d in enumerate(dates)]
        for u, d in zip(self.units, dates):
            u.append(d)
            if d is None:
                self.undated.append(u[0] + 1)
        known = [d for d in dates if d]
        up = sum(1 for x, y in zip(known, known[1:]) if x < y)
        down = sum(1 for x, y in zip(known, known[1:]) if x > y)
        if up > down:
            self.order = "ancien-first"                    # sinon, convention du vault : le plus récent en tête

    def dated(self):
        """Entrées datées, de la plus ancienne à la plus récente (à date égale, la plus éloignée de la tête d'abord)."""
        pos = (lambda u: -u[0]) if self.order == "recent-first" else (lambda u: u[0])
        return sorted((u for u in self.units if u[2] is not None), key=lambda u: (u[2], pos(u)))


def analyse(note, s):
    return [Section(note, t, a, b) for (t, a, b) in note.sections() if t.casefold() in s["sections"]]


# ── plan de rotation ─────────────────────────────────────────────────────────────────────────────────────────

def quarter(d):
    return f"{d.year}-T{(d.month - 1) // 3 + 1}"


def slug_of(path):
    return os.path.splitext(os.path.basename(path))[0]


def plan(note, s):
    """Rend {budget, size, moves: [(section, unit)], blocked, warnings, after_size} sans rien écrire.

    `blocked` : ce qui empêche de revenir sous le budget (lot C d'audit-vault). `warnings` : signalements qui
    n'empêchent pas la rotation (entrées épinglées, liens relatifs dans les entrées déplacées)."""
    ftype = note.fm.get("type", "")
    secs = [] if note.blocked else analyse(note, s)
    bkb = budget_kb(s, ftype, bool(secs) or any(t.casefold() in s["sections"] for t, _, _ in note.sections()))
    res = {"path": note.path, "type": ftype, "size": len(note.raw), "budget": None if bkb is None else bkb * 1024,
           "moves": [], "blocked": [], "warnings": [], "after_size": len(note.raw)}
    if bkb is None or len(note.raw) <= bkb * 1024:
        return res
    if note.blocked:
        res["blocked"].append(note.blocked)
        return res
    if not secs:
        res["blocked"].append("aucune section de journal (" + ", ".join(s["sections"]) + ")")
        return res
    pool = []
    for sec in secs:
        if sec.blocked:
            res["blocked"].append(f"## {sec.title} : {sec.blocked}"); continue
        if sec.undated:
            res["warnings"].append(f"## {sec.title} : entrées sans date en tête, épinglées dans la fiche (lignes "
                                   + ", ".join(map(str, sec.undated[:5])) + ("…" if len(sec.undated) > 5 else "") + ")")
        movable = sec.dated()
        movable = movable[:max(0, len(movable) - s["keep"])]
        pool += [(u[2], k, sec, u) for k, u in enumerate(movable)]
    pool.sort(key=lambda x: (x[0], x[1]))
    size, target = len(note.raw), bkb * 1024 * TARGET
    for _, _, sec, u in pool:
        if size <= target:
            break
        res["moves"].append((sec, u))
        size -= len("\n".join(note.lines[u[0]:u[1]]).encode()) + 1
    res["after_size"] = size
    for _, u in res["moves"]:
        for link in REL_LINK_RE.findall(unit_text(note, u)):
            res["warnings"].append(f"ligne {u[0] + 1} : lien relatif à vérifier après déplacement ({link})")
    if size > bkb * 1024:
        res["blocked"].append(f"reste au-dessus du budget après rotation (~{size // 1024} Ko pour {bkb} Ko)")
    return res


def removal_ranges(p):
    """Plages [a, b) de lignes à retirer : chaque entrée et la ligne vide qui la sépare de sa voisine."""
    out = []
    for sec, u in p["moves"]:
        a, b, line = u[0], u[1], sec.note.line
        while a - 1 > sec.start and not line(a - 1).strip():
            a -= 1
        if a - 1 == sec.start:                   # première entrée : garder le blanc sous le titre, retirer celui d'après
            a = u[0]
            while b < sec.end and not line(b).strip() and any(line(i).strip() for i in range(b, sec.end)):
                b += 1
        out.append([a, b, sec, [u]])
    out.sort(key=lambda x: x[0])
    for prev, cur in zip(out, out[1:]):          # deux plages voisines ne se chevauchent pas
        if cur[0] < prev[1]:
            cur[0] = prev[1]
    return [tuple(x) for x in out]


# ── écriture ─────────────────────────────────────────────────────────────────────────────────────────────────

def unit_text(note, u):
    """Texte de l'entrée pour son journal. En CRLF, chaque ligne garde ou reçoit son \\r (dernière ligne d'un
    fichier sans retour final comprise) : le journal n'a jamais de fin de ligne mixte."""
    lines = note.lines[u[0]:u[1]]
    if note.nl == "\r\n":
        lines = [ln if ln.endswith("\r") else ln + "\r" for ln in lines]
    return "\n".join(lines)


def tight(sec):
    """Vrai si les entrées de la section se suivent sans ligne vide."""
    for a, b in zip(sec.units, sec.units[1:]):
        if a[1] < b[0]:
            return False
    return True


def journal_path(note, d):
    return os.path.join(os.path.dirname(note.path), "journal", f"{slug_of(note.path)}-{quarter(d)}.md")


def new_journal(note, period, nl):
    title = next((note.line(i) for i in range(note.body_start, len(note.lines))
                  if not note.fence[i] and note.line(i).startswith("# ")), "")
    lock = " 🔒" if "🔒" in title else ""
    fm = ["---", "type: journal", f'source: "[[{slug_of(note.path)}]]"', f"periode: {period}"]
    for key, val in note.fm.items():
        if key.casefold() in ("sensibilité", "sensibilite", "confidentiel"):
            fm.append(f"{key}: {val}")
    fm += ["---", "", f"# Journal {slug_of(note.path)} : {period}{lock}", ""]
    return nl.join(fm) + nl


def insert_units(existing, texts, recent_first, sep):
    """Ajoute les entrées au bon bout du journal : en tête pour un journal récent-d'abord, en fin sinon.

    Les lignes gardent leur `\\r` éventuel (découpe sur '\\n') : on ne joint et ne termine qu'avec '\\n'.
    """
    lines = existing.split("\n")
    block = sep.join(texts)
    if recent_first:
        i = 0
        if lines and lines[0].lstrip("﻿").rstrip("\r") == "---":
            i = next((k for k in range(1, len(lines)) if lines[k].rstrip("\r") == "---"), 0) + 1
        while i < len(lines) and not lines[i].strip():
            i += 1
        if i < len(lines) and lines[i].startswith("# "):
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
        head, rest = "\n".join(lines[:i]), "\n".join(lines[i:])
        if head and not head.endswith("\n"):
            head += "\n"
        return head + block + (sep + rest if rest.strip() else "\n")
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines) + sep + block + "\n"


def index_lines(note_lines, slugs, nl):
    """Index `## Journaux` en fin de fiche : on ajoute les liens manquants, on ne réécrit rien d'existant."""
    cr = "\r" if nl == "\r\n" else ""
    lines = list(note_lines)
    flags, _, _ = fences(lines)
    i = next((k for k, ln in enumerate(lines) if not flags[k][0] and ln.strip() == "## Journaux"), None)
    if i is not None:
        j, have = i + 1, set()
        while j < len(lines) and not (not flags[j][0] and H12_RE.match(lines[j].rstrip("\r"))):
            have |= {x.strip() for x in re.findall(r"\[\[([^\]|#]+)", lines[j])}; j += 1
        missing = sorted(set(slugs) - have, reverse=True)
        if not missing:
            return lines
        k = i + 1
        while k < j and not lines[k].strip():
            k += 1
        new = [f"- [[{x}]]{cr}" for x in missing]
        if k == j:                                         # section vide : liens, puis ligne vide ou fin de fichier
            head = lines[:i + 1]
            if cr and not head[-1].endswith("\r"):
                head[-1] += "\r"
            return head + [cr] + new + ([cr] + lines[j:] if j < len(lines) else [""])
        return lines[:k] + new + lines[k:]
    while lines and not lines[-1].strip():
        lines.pop()
    if cr and lines and not lines[-1].endswith("\r"):
        lines[-1] += "\r"                                  # fichier sans retour final : on clôt sa dernière ligne
    return lines + [cr, f"## Journaux{cr}", cr] + [f"- [[{x}]]{cr}" for x in sorted(set(slugs), reverse=True)] + [""]


def nonblank(text):
    return Counter(ln.rstrip("\r").rstrip() for ln in text.split("\n") if ln.strip())


STRUCTURE_LABELS = {x.casefold() for x in (
    "Suivi", "Journal", "Journaux", "Réunions", "Discussions", "Notes", "Historique", "État", "État courant",
    "Décisions", "Décisions clés", "Apprentissages", "À faire", "Todos", "Contexte", "Brief", "Objectif",
    "Points de vigilance", "Sources", "Interlocuteurs", "Questions", "Avancement", "Log", "Échanges")}
LIST_PREFIX_RE = re.compile(r"^\s*([-*+]|\d+[.)])\s+(\[.\]\s+)?")
HEADING_RE = re.compile(r"^\s*#{1,6}\s+(.*)$")


def missing_lines(before_texts, after_texts, loose=False):
    """Lignes non vides d'avant absentes d'après. `loose` tolère, pour une restructuration assistée :
    - un titre d'étiquette de structure (STRUCTURE_LABELS : Suivi, Réunions…), ou dont le texte réapparaît ;
    - une ligne d'au moins 12 caractères (hors puce) contenue telle quelle dans une ligne d'après, complétée ;
    - une ligne plus courte seulement si une ligne d'après a exactement le même texte hors puce."""
    need, have = Counter(), Counter()
    for t in before_texts:
        need += nonblank(t)
    for t in after_texts:
        have += nonblank(t)
    miss = need - have
    if not loose or not miss:
        return sorted(miss.elements())
    pool = [ln.rstrip("\r") for t in after_texts for ln in t.split("\n") if ln.strip()]
    cores = {LIST_PREFIX_RE.sub("", ln).strip() for ln in pool}
    out = []
    for ln in miss.elements():
        h = HEADING_RE.match(ln)
        if h:
            text = h.group(1).strip()
            label = re.sub(r"[^\w\s]", "", text).strip().casefold()
            if label in STRUCTURE_LABELS or any(text in p for p in pool):
                continue
            out.append(ln); continue
        core = LIST_PREFIX_RE.sub("", ln).strip()
        if core in cores or (len(core) >= 12 and any(core in p for p in pool)):
            continue
        out.append(ln)
    return sorted(out)


def state_dir():
    base = os.environ.get("XDG_STATE_HOME") or os.path.join(os.path.expanduser("~"), ".local", "state")
    return os.path.join(base, "second-cerveau", "rotation", dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f"))


def read_text(path):
    with open(path, "rb") as fh:
        return fh.read().decode("utf-8")


def _default_mode():
    um = os.umask(0); os.umask(um)
    return 0o666 & ~um


def prepare(path, text, mode=None):
    """Écrit le contenu dans un temporaire du même dossier, fsync et droits compris. Rend son chemin."""
    d = os.path.dirname(path)
    os.makedirs(d, exist_ok=True)
    if mode is None:
        mode = stat.S_IMODE(os.stat(path).st_mode) if os.path.exists(path) else _default_mode()
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".rotation-")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(text.encode("utf-8"))
            fh.flush(); os.fsync(fh.fileno())
        os.chmod(tmp, mode)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise
    return tmp


def commit_file(tmp, path):
    """Remplacement atomique, puis fsync du dossier."""
    os.replace(tmp, path)
    try:
        dfd = os.open(os.path.dirname(path), os.O_RDONLY)
        try:
            os.fsync(dfd)
        finally:
            os.close(dfd)
    except OSError:
        pass


def atomic_write(path, text, mode=None, guard=None):
    """prepare, puis `guard()` (contrôle de modification concurrente) juste avant le remplacement."""
    tmp = prepare(path, text, mode)
    try:
        if guard:
            guard()
        commit_file(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def _before_write():
    """Point d'accroche des tests (écriture concurrente simulée)."""


def git(vault, *args):
    try:
        r = subprocess.run(["git", *args], cwd=vault, capture_output=True, text=True, timeout=20)
        return r.returncode, (r.stdout + r.stderr).strip()
    except Exception as e:
        return 1, str(e)


def git_commit(vault, paths, msg, only_dirty=False):
    rel = [os.path.relpath(p, vault) for p in paths if os.path.exists(p)]
    if not rel:
        return None
    if only_dirty:
        code, out = git(vault, "status", "--porcelain", "--", *rel)
        if code or not out.strip():
            return None
    git(vault, "add", "--", *rel)
    code, out = git(vault, "commit", "-q", "-m", msg, "--", *rel)
    return None if code == 0 else f"commit git non fait : {out.splitlines()[-1] if out else code}"


def apply(note, p, vault):
    """Écrit la rotation. Rend {written, backup, warnings} ; lève RuntimeError si un contrôle échoue."""
    nl = note.nl
    cr = "\r" if nl == "\r\n" else ""
    ranges = removal_ranges(p)
    dests = {}
    for a, b, sec, units in ranges:
        sep = "\n" if tight(sec) else "\n" + cr + "\n"     # les entrées finissent déjà par leur \r éventuel
        for u in sorted(units, key=lambda u: u[0]):
            path = journal_path(note, u[2])
            dests.setdefault(path, {"texts": [], "recent": sec.order == "recent-first", "sep": sep, "period": quarter(u[2])})
            dests[path]["texts"].append(unit_text(note, u))
    before = {path: (read_text(path) if os.path.exists(path) else None) for path in dests}
    after = {}
    for path, d in dests.items():
        base = before[path] if before[path] is not None else new_journal(note, d["period"], nl)
        after[path] = insert_units(base, d["texts"], d["recent"], d["sep"])
    # fiche réduite, puis index `## Journaux`
    reduced, removed, last = [], [], 0
    for a, b, _, _ in ranges:
        reduced += note.lines[last:a]; removed.append((len(reduced), note.lines[a:b])); last = b
    reduced += note.lines[last:]
    new_note = "\n".join(index_lines(reduced, sorted({slug_of(x) for x in dests}), nl))
    # contrôles : la fiche réduite, entrées réinsérées, redonne l'original à l'octet près
    recon, last = [], 0
    for pos, block in removed:
        recon += reduced[last:pos] + block; last = pos
    recon += reduced[last:]
    if "\n".join(recon) != note.text:
        raise RuntimeError("reconstruction de la fiche impossible à l'identique")
    for path, d in dests.items():
        for t in d["texts"]:
            if t not in after[path]:
                raise RuntimeError(f"entrée absente de {path}")
    lost = missing_lines([note.text] + [t for t in before.values() if t], [new_note] + list(after.values()))
    if lost:
        raise RuntimeError(f"{len(lost)} ligne(s) perdue(s), par exemple : {lost[0][:80]}")

    def unchanged():
        if not note.same_on_disk():
            raise RuntimeError("fiche modifiée pendant la rotation : rien n'est écrit")
        for path in dests:
            now = read_text(path) if os.path.exists(path) else None
            if now != before[path]:
                raise RuntimeError(f"{os.path.relpath(path, vault)} modifié pendant la rotation : rien n'est écrit")

    # sauvegarde hors vault
    unchanged()
    bdir = state_dir()
    for path in [note.path] + [x for x in dests if before[x] is not None]:
        dst = os.path.join(bdir, os.path.relpath(path, vault))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(path, dst)
    warnings = []
    is_git = git(vault, "rev-parse", "--is-inside-work-tree")[0] == 0
    touched = [note.path] + list(dests)
    _before_write()
    unchanged()                                  # avant le commit « avant rotation » : pas de commit si on annule
    if is_git:
        w = git_commit(vault, touched, f"avant rotation du journal : {slug_of(note.path)}", only_dirty=True)
        if w: warnings.append(w)
    def dest_unchanged(path):
        def guard():
            now = read_text(path) if os.path.exists(path) else None
            if now != before[path]:
                raise RuntimeError(f"{os.path.relpath(path, vault)} modifié pendant la rotation : rien n'est écrit")
        return guard

    def note_unchanged():
        if not note.same_on_disk():
            raise RuntimeError("fiche modifiée pendant la rotation : rien n'est écrit")

    written = []
    try:
        for path in dests:                       # destinations d'abord : un arrêt brutal duplique, il ne perd pas
            atomic_write(path, after[path], guard=dest_unchanged(path)); written.append(path)
        for path in dests:
            got = read_text(path)
            if any(t not in got for t in dests[path]["texts"]):
                raise RuntimeError(f"relecture de {os.path.relpath(path, vault)} incomplète")
        # contrôle des octets de la fiche après fsync du temporaire, juste avant le remplacement
        atomic_write(note.path, new_note, note.mode, guard=note_unchanged); written.append(note.path)
    except BaseException:
        for path in written:                     # restauration depuis la sauvegarde
            src = os.path.join(bdir, os.path.relpath(path, vault))
            if os.path.exists(src):
                shutil.copy2(src, path)
            elif before.get(path) is None and os.path.exists(path):
                os.remove(path)
        raise
    if is_git:
        w = git_commit(vault, touched, f"rotation du journal : {slug_of(note.path)} ({len(p['moves'])} entrées)")
        if w: warnings.append(w)
    return {"written": [os.path.relpath(x, vault) for x in written], "backup": bdir, "warnings": p["warnings"] + warnings}


# ── parcours du vault ────────────────────────────────────────────────────────────────────────────────────────

def candidates(vault, s):
    smallest = min(list(s["budgets"].values()) + [s["default_kb"]]) * 1024
    for r, dirs, files in os.walk(vault):
        rel = os.path.relpath(r, vault).replace(os.sep, "/") + "/"
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "journal"]
        if rel != "./" and any(rel.startswith(x) for x in SKIP_DIRS + tuple(s["exclude"])):
            dirs[:] = []; continue
        for fn in files:
            p = os.path.join(r, fn)
            if fn.endswith(".md") and fn not in ("CLAUDE.md", "README.md") and os.path.getsize(p) > smallest:
                yield p


def check(vault):
    s = settings(vault)
    over = []
    for p in candidates(vault, s):
        try:
            note = Note(p)
        except (UnicodeDecodeError, OSError):
            continue
        if note.fm.get("type") == "journal":
            continue
        r = plan(note, s)
        if r["budget"] and r["size"] > r["budget"]:
            over.append({"path": os.path.relpath(p, vault), "type": r["type"], "kb": r["size"] // 1024,
                         "budget_kb": r["budget"] // 1024, "entries": len(r["moves"]),
                         "after_kb": r["after_size"] // 1024, "blocked": r["blocked"], "warnings": r["warnings"]})
    over.sort(key=lambda x: -x["kb"])
    return {"vault": vault, "rotation": s["rotation"], "over": over}


def describe(note, p, vault):
    moves = {}
    for _, u in p["moves"]:
        key = os.path.relpath(journal_path(note, u[2]), vault)
        moves[key] = moves.get(key, 0) + 1
    return {"path": os.path.relpath(note.path, vault), "kb": p["size"] // 1024,
            "budget_kb": None if p["budget"] is None else p["budget"] // 1024,
            "after_kb": p["after_size"] // 1024, "moves": moves, "blocked": p["blocked"], "warnings": p["warnings"]}


def section_links(vault, note):
    """Liens `[[slug#…]]` du vault vers la fiche : signalés, jamais réécrits."""
    slug, hits = slug_of(note.path), []
    pat = re.compile(r"\[\[" + re.escape(slug) + r"#([^\]|]+)")
    for r, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fn in files:
            if fn.endswith(".md"):
                try:
                    with open(os.path.join(r, fn), encoding="utf-8", errors="ignore") as fh:
                        found = list(pat.finditer(fh.read()))
                    for m in found:
                        hits.append(f"{os.path.relpath(os.path.join(r, fn), vault)} : [[{slug}#{m.group(1)}]]")
                except OSError:
                    pass
    return hits


def main(argv):
    if not argv or argv[0] not in ("check", "rotate", "verify"):
        print(__doc__); return 2
    cmd, args = argv[0], argv[1:]

    def opt(name):
        if name in args:
            i = args.index(name)
            if i + 1 >= len(args) or args[i + 1].startswith("--"):
                raise SystemExit(f"{name} attend une valeur")
            v = args[i + 1]; del args[i:i + 2]; return v
        return None

    def flag(name):
        if name in args:
            args.remove(name); return True
        return False

    if cmd == "verify":
        loose = flag("--loose")
        if "--before" not in args or "--after" not in args:
            print("usage : verify [--loose] --before A… --after B…"); return 2
        i, j = args.index("--before"), args.index("--after")
        bef = args[i + 1:j] if i < j else args[i + 1:]
        aft = args[j + 1:] if j > i else args[j + 1:i]
        if not bef or not aft:
            print("usage : verify [--loose] --before A… --after B…"); return 2
        miss = missing_lines([read_text(p) for p in bef], [read_text(p) for p in aft], loose)
        print(json.dumps({"ok": not miss, "missing": miss}, ensure_ascii=False, indent=1))
        return 0 if not miss else 1
    vault = opt("--vault")
    if cmd == "check":
        summary = flag("--summary")
        vault = vault or vault_root(os.getcwd())
        if not vault:
            return 0
        r = check(os.path.realpath(vault))
        if summary:
            if r["over"]:
                big = r["over"][0]
                print(f"{len(r['over'])} fiche(s) au-dessus de leur budget de taille (la plus lourde : "
                      f"{big['path']}, {big['kb']} Ko pour {big['budget_kb']} Ko)")
        else:
            print(json.dumps(r, ensure_ascii=False, indent=1))
        return 0
    do_apply, force, allf = flag("--apply"), flag("--force"), flag("--all")
    files = [os.path.realpath(a) for a in args]
    if allf:
        root = vault or vault_root(os.getcwd())
        if not root:
            print("--all : vault introuvable, préciser --vault"); return 2
        root = os.path.realpath(root)
        files = [os.path.join(root, x["path"]) for x in check(root)["over"] if x["entries"]]
    out, code = [], 0
    for f in files:
        v = vault_root(f)
        if not v:
            out.append({"path": f, "error": "hors d'un vault"}); code = 1; continue
        s = settings(v)
        if do_apply and not (s["rotation"] or force):
            out.append({"path": f, "error": "JOURNAL_ROTATION=1 absent de _Meta/hooks.conf (ou --force)"}); code = 1; continue
        try:
            note = Note(f)
        except (UnicodeDecodeError, OSError) as e:
            out.append({"path": os.path.relpath(f, v), "error": f"illisible : {e.__class__.__name__}"}); code = 1; continue
        p = plan(note, s)
        d = describe(note, p, v)
        if p["moves"]:
            d["section_links"] = section_links(v, note)
        if do_apply and p["moves"]:
            try:
                d.update(apply(note, p, v))
            except (RuntimeError, OSError, ValueError) as e:     # ValueError : journal existant non UTF-8
                d["error"] = str(e) if isinstance(e, RuntimeError) else f"{e.__class__.__name__} : {e}"; code = 1
        d["mode"] = "écrit" if do_apply and p["moves"] and "error" not in d else "simulation"
        out.append(d)
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
