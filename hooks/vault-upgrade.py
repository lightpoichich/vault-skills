#!/usr/bin/env python3
"""vault-upgrade.py · mise à niveau d'un vault installé par `installer`, sans modèle de langage.

  vault-upgrade.py check  --vault V [--summary]     état de chaque fichier ou bloc géré, migrations en attente (JSON)
  vault-upgrade.py stamp  --vault V [--apply]       pose ou rafraîchit la fiche d'installation `_Meta/installation.md`
  vault-upgrade.py apply  --vault V [--apply]       remplace le remplaçable, applique les migrations, met la fiche d'installation à jour
  vault-upgrade.py accept --vault V [--apply] UNITÉ…   déclare une fusion faite ou un ajout refusé : la version actuelle du gabarit est intégrée

Simulation par défaut ; `--apply` écrit.

Unités gérées. Une unité est un fichier copié tel quel à l'installation, ou un bloc entre balises
`<!-- socle second-cerveau : début {id} -->` et `<!-- socle second-cerveau : fin {id} -->` dans un fichier
généré depuis le plan. Le texte hors balises n'est jamais lu ni touché.
  - copie : `_Meta/hooks.conf`, posé aussi dans un vault qui ne l'a jamais eu ;
  - bloc  : `CLAUDE.md` racine, `_Meta/Schema.md`.
La persona Chief of Staff (`_personas/cos/`, brief compris) appartient à l'utilisateur dès l'installation, comme tout
`_personas/` : elle se personnalise dès l'usage. Gérée jusqu'à la 5.2.x, ses empreintes héritées sortent de la fiche
d'installation sans signal.

La fiche d'installation garde, par unité, l'empreinte du gabarit intégré : celui posé à l'installation, ou celui retenu
par la dernière fusion (`accept`). Trois cas décident sans copie de référence dans le vault :
  - contenu du vault identique au gabarit intégré, gabarit changé depuis : remplaçable ;
  - contenu du vault modifié, gabarit inchangé : personnalisé, rien à faire ;
  - contenu du vault modifié, gabarit changé : fusion à proposer, jamais écrite par ce script.
Sans fiche d'installation (vault installé avant ce mécanisme), une unité identique au gabarit est notée intégrée ; les
autres restent « inconnu » jusqu'à une fusion revue et acceptée. Rien n'est écrasé.

Migrations : déclarées dans MIGRATIONS (identifiant, version, contrôle, action), idempotentes, inscrites dans
la fiche d'installation une fois appliquées. Avant tout remplacement, copie des fichiers touchés dans
${XDG_STATE_HOME:-~/.local/state}/second-cerveau/mise-a-niveau/{horodatage}/.
Dépendances : python3.
"""
import sys
sys.dont_write_bytecode = True                             # pas de __pycache__ dans le dossier du plugin
import argparse, datetime as dt, hashlib, json, os, re, shutil, tempfile

PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(PLUGIN, "skills", "installer", "assets")
STAMP = "_Meta/installation.md"

# (chemin dans le vault, chemin dans assets/) ; un dossier gère tous ses fichiers, présents et futurs.
COPY_UNITS = [
    ("_Meta/hooks.conf", "hooks/hooks.conf"),
]
BLOCK_FILES = [
    ("CLAUDE.md", "vault-claude-template.md"),
    ("_Meta/Schema.md", "schema-template.md"),
]
# Préfixes rendus à l'utilisateur : une empreinte héritée sous l'un d'eux est ignorée à la lecture de la fiche
# d'installation, puis retirée à sa prochaine écriture.
RELEASED = ("_personas/",)
# Effet d'un ajout, montré dans le plan avant le go : poser un fichier de réglages change le comportement du vault.
EFFECTS = {
    "_Meta/hooks.conf": "réglages par défaut des automatismes, dont la rotation des journaux de fiche "
                        "(JOURNAL_ROTATION=1) ; refus durable par `accept`",
}
BLOCK_RE = re.compile(r"<!-- socle second-cerveau : début ([a-z0-9-]+) -->\n(.*?)<!-- socle second-cerveau : fin \1 -->",
                      re.S)

# Noms de skills retirés et leur remplaçant, repris de skills/audit-vault/references/checks.md (table « Skills
# retirés du plugin ») ; dev/tests/test_vault_upgrade.py vérifie que les deux tables concordent.
RETIRED = {
    "sync-repo": "sync-vault",
    "nouveau-projet": "structurer",
    "gerer-area": "structurer",
    "import-note": "ranger",
    "extraire-trame": "ranger",
    "kickstart-persona": "assistants",
    "vault-skill-creator": "assistants",
    "interview-vault": "/second-cerveau:installer",
    "kickstart-vault": "/second-cerveau:installer",
}

LABELS = {
    "a-jour": "à jour",
    "remplacable": "remplaçable : jamais modifié depuis l'intégration, gabarit changé",
    "fusion": "personnalisé et gabarit changé : fusion à proposer",
    "personnalise": "personnalisé, gabarit inchangé",
    "absent": "absent du vault",
    "nouveau": "nouveau fichier du gabarit",
    "retire": "retiré du gabarit",
    "inconnu": "inconnu : pas d'empreinte dans la fiche d'installation",
    "balises-absentes": "balises absentes",
}
ACTIONABLE = {"remplacable", "fusion", "nouveau", "inconnu", "balises-absentes"}
# Le bilan de démarrage ne signale que ce qu'une mise à niveau changerait : pas de bruit permanent pour un
# « inconnu » ou des balises absentes, qui attendent une revue assistée.
NOTICE = {"remplacable", "fusion", "nouveau"}


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except (OSError, UnicodeDecodeError):
        return None


def write_atomic(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mode = os.stat(path).st_mode & 0o777 if os.path.exists(path) else 0o644
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix=".upgrade-")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(text)
        fh.flush()
        os.fsync(fh.fileno())
    os.chmod(tmp, mode)
    os.replace(tmp, path)


def plugin_version():
    try:
        with open(os.path.join(PLUGIN, ".claude-plugin", "plugin.json"), encoding="utf-8") as fh:
            return json.load(fh).get("version", "")
    except (OSError, ValueError):
        return ""


# ---------- fiche d'installation

def load_stamp(vault):
    text = read(os.path.join(vault, STAMP))
    if text is None:
        return None
    m = re.search(r"```json\n(.*?)\n```", text, re.S)
    try:
        data = json.loads(m.group(1)) if m else {}
    except ValueError:
        data = {}
    data["unites"] = {k: v for k, v in (data.get("unites") or {}).items() if not k.startswith(RELEASED)}
    data.setdefault("migrations", [])
    return data


def render_stamp(data):
    today = dt.date.today().isoformat()
    body = json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True)
    return (f"---\ntype: moc\ntopic: installation\nupdated: {today}\n---\n\n"
            "# Installation du plugin second-cerveau\n\n"
            "> Tenu par `vault-upgrade.py`, à ne pas modifier à la main. Il sert à la mise à niveau du vault : pour\n"
            "> chaque fichier ou bloc posé par l'installation, l'empreinte du gabarit intégré.\n\n"
            f"- Version du plugin intégrée : {data.get('version') or 'inconnue'}\n"
            f"- Dernière écriture : {today}\n"
            f"- Migrations appliquées : {', '.join(data.get('migrations') or []) or 'aucune'}\n\n"
            f"```json\n{body}\n```\n")


# ---------- unités

def copy_units():
    """(clé, chemin vault relatif, chemin gabarit absolu, dossier racine de l'unité dans le vault)."""
    out = []
    for vrel, arel in COPY_UNITS:
        src = os.path.join(ASSETS, arel)
        if os.path.isdir(src):
            for root, dirs, files in os.walk(src):
                dirs.sort()
                for fn in sorted(files):
                    p = os.path.join(root, fn)
                    rel = os.path.relpath(p, src).replace(os.sep, "/")
                    out.append((f"{vrel}/{rel}", f"{vrel}/{rel}", p, vrel))
        elif os.path.isfile(src):
            out.append((vrel, vrel, src, os.path.dirname(vrel)))
    return out


def blocks_of(text):
    return {m.group(1): m.group(2) for m in BLOCK_RE.finditer(text or "")}


def block_units():
    """(clé, chemin vault relatif, id, contenu du bloc dans le gabarit actuel)."""
    out = []
    for vrel, arel in BLOCK_FILES:
        for bid, content in blocks_of(read(os.path.join(ASSETS, arel))).items():
            out.append((f"{vrel}#{bid}", vrel, bid, content))
    return out


def decide(current, template, base):
    """Cas d'une unité présente dans le vault et dans le gabarit."""
    if current == template:
        return "a-jour"
    if base is None:
        return "inconnu"
    if sha(current) == base:
        return "remplacable"
    return "personnalise" if sha(template) == base else "fusion"


def survey(vault, stamp):
    units = (stamp or {}).get("unites", {})
    rows = []
    seen = set()
    for key, vrel, src, root in copy_units():
        seen.add(key)
        template = read(src)
        current = read(os.path.join(vault, vrel))
        base = units.get(key, {}).get("empreinte")
        if current is None:
            # Jamais intégré (aucune empreinte, fiche d'installation absente comprise) et dossier présent : à ajouter.
            # Intégré puis supprimé, ou refusé par `accept` : choix de l'utilisateur, respecté.
            fresh = not units.get(key, {}).get("empreinte") and os.path.isdir(os.path.join(vault, root))
            case = "nouveau" if fresh else "absent"
        else:
            case = decide(current, template, base)
        rows.append({"unite": key, "mode": "copie", "fichier": vrel, "cas": case, "etat": LABELS[case],
                     "_template": template, "_current": current})
    for key, vrel, bid, template in block_units():
        seen.add(key)
        text = read(os.path.join(vault, vrel))
        base = units.get(key, {}).get("empreinte")
        if text is None:
            case, current = "absent", None
        else:
            current = blocks_of(text).get(bid)
            case = "balises-absentes" if current is None else decide(current, template, base)
        rows.append({"unite": key, "mode": "bloc", "fichier": vrel, "bloc": bid, "cas": case, "etat": LABELS[case],
                     "_template": template, "_current": current})
    for key, info in units.items():
        if key not in seen:
            rows.append({"unite": key, "mode": info.get("mode", "copie"), "fichier": key.split("#")[0],
                         "cas": "retire", "etat": LABELS["retire"], "_template": None, "_current": None})
    return rows


# ---------- migrations

def _procedure_files(vault):
    """`CLAUDE.md` racine, `CLAUDE.md` des personas, fichiers markdown des skills du vault ; une fois par
    fichier réel (une persona peut lier le skill d'une autre), jamais hors du vault."""
    real_vault = os.path.realpath(vault)
    cands = [os.path.join(vault, "CLAUDE.md")]
    personas = os.path.join(vault, "_personas")
    if os.path.isdir(personas):
        for p in sorted(os.listdir(personas)):
            cands.append(os.path.join(personas, p, "CLAUDE.md"))
    roots = [os.path.join(vault, ".claude", "skills")]
    if os.path.isdir(personas):
        roots += [os.path.join(personas, p, ".claude", "skills") for p in sorted(os.listdir(personas))]
    for r in roots:
        for root, dirs, files in os.walk(r, followlinks=True):
            dirs.sort()
            cands += [os.path.join(root, f) for f in sorted(files) if f.endswith(".md")]
    seen, out = set(), []
    for c in cands:
        real = os.path.realpath(c)
        if os.path.isfile(real) and real.startswith(real_vault + os.sep) and real not in seen:
            seen.add(real)
            out.append(real)
    return out


def _rename_hits(text):
    return {old: text.count(f"`{old}`") for old in RETIRED if f"`{old}`" in text}


def check_skill_names(vault):
    hits = []
    for p in _procedure_files(vault):
        found = _rename_hits(read(p) or "")
        if found:
            hits.append({"fichier": os.path.relpath(p, os.path.realpath(vault)), "noms": found})
    return hits


def _rewrite_names(text):
    for old, rep in RETIRED.items():
        text = text.replace(f"`{old}`", f"`{rep}`")
    return text


# Hooks recopiés dans le vault par `kickstart-vault` jusqu'à la 2.6.x : depuis la 2.7.0, le plugin les fournit, et une
# copie locale les fait tourner deux fois dans une session lancée à la racine.
LOCAL_HOOK_SCRIPTS = ("vault-health.sh", "vault-note-guard.sh")
LOCAL_HOOK_RE = re.compile(r"(?:^|[/\"'])\.claude/hooks/(?:" + "|".join(re.escape(n) for n in LOCAL_HOOK_SCRIPTS) + r")\b")


def _settings(vault):
    return os.path.join(vault, ".claude", "settings.json")


def _strip_local_hooks(text):
    """Retire de `.claude/settings.json` les entrées qui appellent une copie locale ; rend (texte, nombre retiré).
    Le reste du fichier (permissions, réglages, autres hooks) est gardé ; un JSON illisible n'est pas touché."""
    try:
        data = json.loads(text)
    except ValueError:
        return text, 0
    hooks = data.get("hooks") if isinstance(data, dict) else None
    if not isinstance(hooks, dict):
        return text, 0
    removed = 0
    for event in list(hooks):
        groups = hooks[event]
        if not isinstance(groups, list):
            continue
        kept_groups = []
        for g in groups:
            inner = g.get("hooks") if isinstance(g, dict) else None
            if not isinstance(inner, list):
                kept_groups.append(g)
                continue
            kept = [h for h in inner if not (isinstance(h, dict) and LOCAL_HOOK_RE.search(str(h.get("command", ""))))]
            removed += len(inner) - len(kept)
            if kept or not inner:
                kept_groups.append(dict(g, hooks=kept))
        if kept_groups:
            hooks[event] = kept_groups
        else:
            del hooks[event]
    if not removed:
        return text, 0
    if not hooks:
        del data["hooks"]
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n", removed


def _local_hook_files(vault):
    return [_settings(vault)]


def _local_hook_scripts_to_delete(vault, writes):
    """Copies locales que plus aucun réglage du vault n'appelle, après réécriture de `settings.json`."""
    settings = writes.get(_settings(vault), read(_settings(vault)))
    if settings is not None:
        try:
            json.loads(settings)
        except ValueError:
            return []                                      # réglages illisibles : impossible de savoir qui appelle quoi
    refs = (settings or "") + (read(os.path.join(vault, ".claude", "settings.local.json")) or "")
    out = []
    for name in LOCAL_HOOK_SCRIPTS:
        path = os.path.join(vault, ".claude", "hooks", name)
        if os.path.isfile(path) and f".claude/hooks/{name}" not in refs:
            out.append(path)
    return out


def _local_hook_rewrite(text):
    return _strip_local_hooks(text)[0]


def check_local_hooks(vault):
    hits = []
    text = read(_settings(vault))
    if text is not None:
        new, n = _strip_local_hooks(text)
        if n:
            hits.append({"fichier": ".claude/settings.json", "entrees_retirees": n})
        writes = {_settings(vault): new}
    else:
        writes = {}
    for path in _local_hook_scripts_to_delete(vault, writes):
        hits.append({"fichier": os.path.relpath(path, vault).replace(os.sep, "/"), "action": "supprimé"})
    return hits


MIGRATIONS = [
    {"id": "5.0.0-noms-skills", "version": "5.0.0",
     "description": "noms de skills retirés, entre accents graves, réécrits vers leur remplaçant",
     "controle": check_skill_names, "action": _rewrite_names, "fichiers": _procedure_files},
    {"id": "5.3.0-hooks-locaux", "version": "5.3.0",
     "description": "copies locales de vault-health et vault-note-guard (installations d'avant la 2.7.0) retirées de "
                    ".claude/settings.json puis supprimées : le plugin fournit ces hooks, la copie les doublait",
     "controle": check_local_hooks, "action": _local_hook_rewrite, "fichiers": _local_hook_files,
     "supprimer": _local_hook_scripts_to_delete},
]


def pending_migrations(vault, stamp):
    done = set((stamp or {}).get("migrations", []))
    out = []
    for m in MIGRATIONS:
        if m["id"] in done:
            continue
        hits = m["controle"](vault)
        out.append({"id": m["id"], "version": m["version"], "description": m["description"], "occurrences": hits})
    return out


# ---------- commandes

def public(rows):
    return [{k: v for k, v in r.items() if not k.startswith("_")} for r in rows]


def cmd_check(vault, summary):
    stamp = load_stamp(vault)
    rows = survey(vault, stamp)
    migs = pending_migrations(vault, stamp)
    todo_units = [r for r in rows if r["cas"] in (NOTICE if summary else ACTIONABLE)]
    todo_migs = [m for m in migs if m["occurrences"]]
    out = {"vault": vault, "version_vault": (stamp or {}).get("version"), "version_plugin": plugin_version(),
           "tampon": stamp is not None, "unites": public(rows), "migrations_en_attente": migs,
           "a_faire": bool(todo_units or todo_migs or stamp is None)}
    if not summary:
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return
    if stamp is None:
        print("le plugin ne connaît pas encore les fichiers qu'il a posés dans ce vault : saisir une fois /second-cerveau:installer pour en dresser l'état")
        return
    if not (todo_units or todo_migs):
        return
    counts = {}
    for r in todo_units:
        counts[r["cas"]] = counts.get(r["cas"], 0) + 1
    parts = [f"{n} {LABELS[c].split(' :')[0]}" for c, n in sorted(counts.items())]
    if todo_migs:
        parts.append(f"{len(todo_migs)} migration(s)")
    print(f"mise à niveau disponible, vault {out['version_vault'] or '?'} et plugin {out['version_plugin'] or '?'} : "
          + ", ".join(parts) + " (/second-cerveau:installer)")


def new_stamp_data(vault, stamp, rows, migrations_done):
    """Empreintes du gabarit intégré : inchangées sauf pour une unité identique au gabarit actuel."""
    units = dict((stamp or {}).get("unites", {}))
    for r in rows:
        if r["cas"] == "retire":
            continue
        previous = units.get(r["unite"], {}).get("empreinte")
        units[r["unite"]] = {"mode": r["mode"],
                             "empreinte": sha(r["_template"]) if r["cas"] == "a-jour" else previous}
    return {"version": plugin_version(), "unites": units,
            "migrations": sorted(set((stamp or {}).get("migrations", [])) | set(migrations_done))}


def backup(vault, paths):
    if not paths:
        return None
    base = os.environ.get("XDG_STATE_HOME") or os.path.join(os.path.expanduser("~"), ".local", "state")
    dest = os.path.join(base, "second-cerveau", "mise-a-niveau", dt.datetime.now().strftime("%Y%m%d-%H%M%S"))
    for p in paths:
        if os.path.exists(p):
            target = os.path.join(dest, os.path.relpath(p, vault))
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.copy2(p, target)
    return dest


def cmd_stamp(vault, do_apply):
    stamp = load_stamp(vault)
    rows = survey(vault, stamp)
    data = new_stamp_data(vault, stamp, rows, [])
    if stamp is None:
        # Installation fraîche : toute migration déjà sans objet est notée faite.
        data["migrations"] = sorted(m["id"] for m in MIGRATIONS if not m["controle"](vault))
    out = {"tampon": STAMP, "ecrit": do_apply, "version": data["version"],
           "unites_integrees": sum(1 for u in data["unites"].values() if u.get("empreinte")),
           "unites_inconnues": sorted(k for k, u in data["unites"].items() if not u.get("empreinte"))}
    if do_apply:
        write_atomic(os.path.join(vault, STAMP), render_stamp(data))
    print(json.dumps(out, ensure_ascii=False, indent=1))


def cmd_apply(vault, do_apply):
    stamp = load_stamp(vault)
    rows = survey(vault, stamp)
    plan, writes = [], {}
    for r in rows:
        path = os.path.realpath(os.path.join(vault, r["fichier"]))
        if r["mode"] == "copie" and r["cas"] in ("remplacable", "nouveau"):
            writes[path] = r["_template"]
            step = {"unite": r["unite"], "action": "remplacé" if r["cas"] == "remplacable" else "ajouté"}
            if r["cas"] == "nouveau" and r["unite"] in EFFECTS:
                step["effet"] = EFFECTS[r["unite"]]
            plan.append(step)
        elif r["mode"] == "bloc" and r["cas"] == "remplacable":
            text = writes.get(path, read(path))
            bid = r["bloc"]
            text = BLOCK_RE.sub(lambda m: m.group(0) if m.group(1) != bid else
                                f"<!-- socle second-cerveau : début {bid} -->\n{r['_template']}"
                                f"<!-- socle second-cerveau : fin {bid} -->", text)
            writes[path] = text
            plan.append({"unite": r["unite"], "action": "bloc remplacé"})
    done, deletes = [], []
    for m in pending_migrations(vault, stamp):
        mig = next(x for x in MIGRATIONS if x["id"] == m["id"])
        if m["occurrences"]:
            for p in mig["fichiers"](vault):
                current = writes.get(p, read(p) or "")
                new = mig["action"](current)
                if new != current:
                    writes[p] = new
            if mig.get("supprimer"):
                deletes += [p for p in mig["supprimer"](vault, writes) if p not in deletes]
            plan.append({"migration": m["id"], "description": m["description"],
                         "fichiers": [o["fichier"] for o in m["occurrences"]]})
        done.append(m["id"])
    left = [{"unite": r["unite"], "cas": r["cas"], "etat": r["etat"]} for r in rows
            if r["cas"] in ("fusion", "inconnu", "balises-absentes", "absent", "retire")]
    out = {"ecrit": do_apply, "plan": plan, "a_revoir": left, "sauvegarde": None}
    if do_apply:
        out["sauvegarde"] = backup(vault, list(writes) + deletes)
        for p, text in writes.items():
            write_atomic(p, text)
        for p in deletes:
            os.remove(p)
            parent = os.path.dirname(p)
            if parent != vault and not os.listdir(parent):     # `.claude/hooks/` vidé : retiré aussi
                os.rmdir(parent)
        after = survey(vault, stamp)
        data = new_stamp_data(vault, stamp, after, done)
        write_atomic(os.path.join(vault, STAMP), render_stamp(data))
    print(json.dumps(out, ensure_ascii=False, indent=1))


def cmd_accept(vault, units, do_apply):
    stamp = load_stamp(vault) or {"unites": {}, "migrations": []}
    rows = {r["unite"]: r for r in survey(vault, stamp)}
    unknown = [u for u in units if u not in rows or rows[u]["_template"] is None]
    if unknown:
        sys.exit(f"unité inconnue : {', '.join(unknown)}")
    for u in units:
        stamp["unites"][u] = {"mode": rows[u]["mode"], "empreinte": sha(rows[u]["_template"])}
    stamp["version"] = stamp.get("version") or plugin_version()
    if do_apply:
        write_atomic(os.path.join(vault, STAMP), render_stamp(stamp))
    print(json.dumps({"ecrit": do_apply, "acceptees": units}, ensure_ascii=False, indent=1))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("check", "stamp", "apply", "accept"):
        s = sub.add_parser(name)
        s.add_argument("--vault", required=True)
        if name == "check":
            s.add_argument("--summary", action="store_true", help="une ligne, rien si rien à faire")
        else:
            s.add_argument("--apply", action="store_true", help="écrire ; sans lui, simulation")
        if name == "accept":
            s.add_argument("unites", nargs="+")
    a = ap.parse_args()
    vault = os.path.realpath(os.path.expanduser(a.vault))
    if not os.path.isdir(os.path.join(vault, "_Meta")):
        sys.exit(f"vault introuvable : {vault} n'a pas de dossier _Meta/")
    if a.cmd == "check":
        cmd_check(vault, a.summary)
    elif a.cmd == "stamp":
        cmd_stamp(vault, a.apply)
    elif a.cmd == "apply":
        cmd_apply(vault, a.apply)
    else:
        cmd_accept(vault, a.unites, a.apply)


if __name__ == "__main__":
    main()
