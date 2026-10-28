#!/usr/bin/env python3
"""vault-inventory.py · inventaire d'un lot à ranger dans le vault (mode lot de `ranger`).

  vault-inventory.py scan SOURCE [--vault VAULT] [--label NOM] [--manifeste CHEMIN] [--max-mb 20]

SOURCE est un dossier ou une archive `.zip`. Un export Claude.ai est reconnu sous ses deux formes : une
archive unique (`conversations.json`, `projects.json`), ou le dossier qui réunit le manifeste et une
archive par catégorie (`projects-000.zip` avec `projects/{uuid}.json`, `memories-000.zip`,
`conversations-000.zip`, `light_metadata-000.zip`), forme constatée sur un export réel le 2026-10-28.
Il est découpé en un fichier markdown par projet (description, instructions, mémoire du projet,
fichiers de mémoire du projet), par document de connaissance, par fichier de mémoire hors projet et
par conversation (résumé, messages, outils nommés, sans la réflexion interne). Le manifeste, qui porte
les liens de téléchargement, n'est jamais un élément du lot.

Sans modèle de langage et sans écriture dans le vault, sauf le squelette du manifeste demandé par
`--manifeste`. Les archives sont extraites hors du vault, dans
${XDG_STATE_HOME:-~/.local/state}/second-cerveau/import/{lot}/ : un export brut peut contenir du sensible
et ne doit pas partir avec le git du vault. Un dossier est lu en place.

Chaque élément reçoit une clé stable, posée ensuite en `source:` de la note écrite (ou citée dans
l'entrée de journal d'une fiche) : `{label}:{chemin relatif}` pour un fichier, `claude:projet:{uuid}`,
`claude:document:{uuid}`, `claude:conversation:{uuid}`, `claude:memoire:{chemin}` pour un export Claude.ai. Une clé déjà présente
dans le vault marque l'élément comme importé : relancer le même lot ne duplique rien, à condition de
garder le même `--label`.

Sans `--vault`, le script inventorie seul, sans détection des éléments déjà importés : c'est le cas de
l'entretien d'installation, où l'export Claude.ai se lit avant que le vault n'ait son `_Meta/`.

Sortie : `inventaire.json` dans le dossier du lot (un objet par élément) et un résumé sur la sortie
standard. Format de l'export Claude.ai non documenté par Anthropic : lecture tolérante, champs absents
ignorés. La catégorie `frames` n'a pas encore été observée ; ses fichiers passent en éléments ordinaires.
"""
import argparse, datetime, hashlib, json, os, re, shutil, sys, unicodedata, zipfile

SKIP_DIRS = {".git", "__MACOSX", "node_modules", ".obsidian", ".trash"}
TYPES = {
    ".md": "markdown", ".markdown": "markdown", ".txt": "texte", ".html": "page web", ".htm": "page web",
    ".csv": "tableau", ".xlsx": "tableau", ".xls": "tableau", ".pdf": "pdf",
    ".docx": "document office", ".doc": "document office", ".pptx": "document office", ".odt": "document office",
    ".png": "image", ".jpg": "image", ".jpeg": "image", ".gif": "image", ".webp": "image", ".heic": "image",
    ".json": "json",
}
SENSIBLE = re.compile(r"(contrat|salaire|\bpaie\b|bulletin|mutuelle|\brib\b|\biban\b|banque|bancaire|"
                      r"passeport|identit[eé]|m[eé]dical|sant[eé]|licenciement|rupture|disciplin|confidentiel|"
                      r"password|mot[-_ ]de[-_ ]passe)", re.I)
KEY_RE = re.compile(r"claude:(?:projet|document|conversation|memoire|passation):[0-9A-Za-z-]{4,}")
SOURCE_RE = re.compile(r"^\s*-?\s*source\s*:\s*(.+?)\s*$", re.M)


def slug(text, n=60):
    t = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()
    return (t[:n].strip("-") or "sans-titre")


def state_base():
    base = os.environ.get("XDG_STATE_HOME") or os.path.join(os.path.expanduser("~"), ".local", "state")
    return os.path.join(base, "second-cerveau", "import")


def day(ts):
    """Date AAAA-MM-JJ depuis un epoch, une chaîne ISO ou un tuple de ZipInfo ; vide si illisible."""
    try:
        if isinstance(ts, (int, float)):
            return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
        if isinstance(ts, tuple):
            return "%04d-%02d-%02d" % ts[:3]
        if isinstance(ts, str) and ts:
            return datetime.datetime.fromisoformat(ts.replace("Z", "+00:00")[:32]).strftime("%Y-%m-%d")
    except (ValueError, OverflowError, OSError, TypeError):
        pass
    if isinstance(ts, str) and re.match(r"^\d{4}-\d{2}-\d{2}", ts):
        return ts[:10]
    return ""


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def safe_extract(zpath, dest):
    """Extrait une archive en refusant les chemins absolus et les remontées (`..`). Rend {chemin: date}."""
    dates = {}
    with zipfile.ZipFile(zpath) as zf:
        for info in zf.infolist():
            name = info.filename.replace("\\", "/")
            parts = [p for p in name.split("/") if p not in ("", ".")]
            if not parts or name.startswith("/") or ".." in parts or re.match(r"^[A-Za-z]:", name):
                continue
            target = os.path.join(dest, *parts)
            if info.is_dir():
                os.makedirs(target, exist_ok=True)
                continue
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with zf.open(info) as src, open(target, "wb") as out:
                shutil.copyfileobj(src, out)
            dates[os.path.relpath(target, dest)] = day(info.date_time)
    return dates


def vault_keys(vault):
    """Clés déjà présentes dans le vault : valeurs de `source:` et clés Claude.ai citées n'importe où."""
    found = {}
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in files:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            try:
                with open(p, encoding="utf-8", errors="ignore") as fh:
                    text = fh.read()
            except OSError:
                continue
            rel = os.path.relpath(p, vault)
            for v in SOURCE_RE.findall(text):
                found.setdefault(v.strip().strip("\"'"), rel)
            for k in KEY_RE.findall(text):
                found.setdefault(k, rel)
    return found


def embed(text):
    """Texte inséré sous un titre `##` : ses propres titres descendent de deux niveaux, hors blocs de code."""
    out, fence = [], False
    for line in str(text).strip().splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
        out.append("##" + line if not fence and re.match(r"^#{1,4}\s", line) else line)
    return "\n".join(out)


def message_text(m):
    """Texte lisible d'un message : blocs `text`, outils nommés, pièces jointes. Ni réflexion ni prompt injecté."""
    parts = []
    content = m.get("content")
    if isinstance(content, list) and content:
        for c in content:
            if not isinstance(c, dict):
                continue
            if c.get("type") == "text" and c.get("text"):
                parts.append(c["text"])
            elif c.get("type") == "tool_use" and c.get("name"):
                parts.append(f"> Outil utilisé : {c['name']}")
    text = embed("\n\n".join(parts) or m.get("text") or "")
    for a in m.get("attachments") or []:
        if isinstance(a, dict) and a.get("extracted_content"):
            text += f"\n\n> Pièce jointe « {a.get('file_name', 'sans nom')} » :\n\n{embed(a['extracted_content'])}"
    for f in m.get("files") or []:
        if isinstance(f, dict) and f.get("file_name"):
            text += f"\n\n> Fichier joint sans contenu dans l'export : {f['file_name']}"
    return text.strip()


def load_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def claude_files(root):
    """Fichiers JSON d'un export Claude.ai, par catégorie, quelle que soit la disposition (ancienne archive
    unique ou archives par catégorie : `conversations.json`, `projects/{uuid}.json`, `memories/{uuid}.json`)."""
    found = {"conversations": [], "projects": [], "memories": [], "metadata": []}
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
        parent = os.path.basename(dirpath)
        for fn in sorted(files):
            if not fn.endswith(".json"):
                continue
            p = os.path.join(dirpath, fn)
            if fn == "conversations.json":
                found["conversations"].append(p)
            elif fn == "projects.json" or parent == "projects":
                found["projects"].append(p)
            elif parent == "memories" or fn == "memories.json":
                found["memories"].append(p)
            elif fn in ("users.json", "login_history.json"):
                found["metadata"].append(p)
    return found


def as_list(data):
    if isinstance(data, list):
        return [d for d in data if isinstance(d, dict)]
    return [data] if isinstance(data, dict) else []


def split_claude(root, out):
    """Découpe un export Claude.ai en markdown. Rend la liste des éléments (sans id ni état vault)."""
    items = []
    for d in ("projets", "documents", "conversations", "memoires"):
        os.makedirs(os.path.join(out, d), exist_ok=True)
    files = claude_files(root)
    memories = [m for p in files["memories"] for m in as_list(load_json(p))]
    project_memory = {}
    memory_files_by_project = {}
    other_memory_files = []
    for mem in memories:
        project_memory.update({k: v for k, v in (mem.get("project_memories") or {}).items() if v})
        for mf in mem.get("memory_files") or []:
            if not isinstance(mf, dict) or not mf.get("content"):
                continue
            hit = re.match(r"^/?projects/([0-9A-Za-z-]+)/", mf.get("path") or "")
            if hit:
                memory_files_by_project.setdefault(hit.group(1), []).append(mf)
            else:
                other_memory_files.append(mf)

    for p in [p for f in files["projects"] for p in as_list(load_json(f))]:
        uuid = str(p.get("uuid") or hashlib.sha256(json.dumps(p, sort_keys=True).encode()).hexdigest()[:12])
        name = p.get("name") or "Projet sans nom"
        docs = [d for d in p.get("docs") or [] if isinstance(d, dict)]
        lines = [f"# {name}", "", f"- Clé : claude:projet:{uuid}",
                 f"- Créé le {day(p.get('created_at')) or '?'}, modifié le {day(p.get('updated_at')) or '?'}", ""]
        if p.get("description"):
            lines += ["## Description", "", embed(p["description"]), ""]
        if p.get("prompt_template"):
            lines += ["## Instructions du projet", "", embed(p["prompt_template"]), ""]
        if project_memory.get(uuid):
            lines += ["## Mémoire du projet (Claude.ai)", "", embed(project_memory[uuid]), ""]
        for mf in memory_files_by_project.get(uuid, []):
            lines += [f"## Fichier de mémoire {mf.get('path')} (modifié le {day(mf.get('updated_at')) or '?'})", "",
                      embed(mf["content"]), ""]
        if docs:
            lines += ["## Documents de connaissance", ""]
        for d in docs:
            duuid = str(d.get("uuid") or hashlib.sha256((uuid + str(d.get("filename"))).encode()).hexdigest()[:12])
            fname = d.get("filename") or "document"
            dpath = os.path.join(out, "documents", f"{slug(name, 30)}-{slug(fname, 40)}-{duuid[:8]}.md")
            with open(dpath, "w", encoding="utf-8") as fh:
                fh.write(f"# {fname}\n\n- Clé : claude:document:{duuid}\n- Projet : {name} (claude:projet:{uuid})\n\n"
                         + str(d.get("content") or "").strip() + "\n")
            lines.append(f"- {fname} : `documents/{os.path.basename(dpath)}`")
            items.append({"cle": f"claude:document:{duuid}", "type": "document claude", "titre": f"{name} · {fname}",
                          "chemin": dpath, "date": day(d.get("created_at")) or day(p.get("updated_at")),
                          "projet": f"claude:projet:{uuid}"})
        ppath = os.path.join(out, "projets", f"{slug(name)}-{uuid[:8]}.md")
        with open(ppath, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines).rstrip() + "\n")
        item = {"cle": f"claude:projet:{uuid}", "type": "projet claude", "titre": name, "chemin": ppath,
                "date": day(p.get("updated_at")) or day(p.get("created_at")), "documents": len(docs),
                "instructions": bool(p.get("prompt_template")), "memoire": bool(project_memory.get(uuid))}
        if p.get("is_starter_project"):
            item["exemple"] = True
        items.append(item)

    for mem in memories:
        if mem.get("conversations_memory"):
            mpath = os.path.join(out, "memoires", "memoire-generale.md")
            with open(mpath, "w", encoding="utf-8") as fh:
                fh.write("# Mémoire générale (Claude.ai)\n\n- Clé : claude:memoire:generale\n\n"
                         + str(mem["conversations_memory"]).strip() + "\n")
            items.append({"cle": "claude:memoire:generale", "type": "mémoire claude",
                          "titre": "Mémoire générale", "chemin": mpath, "date": ""})
    for mf in other_memory_files:
        path = mf.get("path") or "memoire"
        key = "claude:memoire:" + slug(path, 80)
        mpath = os.path.join(out, "memoires", slug(path, 80) + ".md")
        with open(mpath, "w", encoding="utf-8") as fh:
            fh.write(f"# Mémoire {path} (Claude.ai)\n\n- Clé : {key}\n\n" + str(mf["content"]).strip() + "\n")
        items.append({"cle": key, "type": "mémoire claude", "titre": f"Mémoire {path}", "chemin": mpath,
                      "date": day(mf.get("updated_at"))})

    for c in [c for f in files["conversations"] for c in as_list(load_json(f))]:
        uuid = str(c.get("uuid") or hashlib.sha256(json.dumps(c, sort_keys=True).encode()).hexdigest()[:12])
        name = c.get("name") or "Conversation sans titre"
        msgs = [m for m in c.get("chat_messages") or [] if isinstance(m, dict)]
        lines = [f"# {name}", "", f"- Clé : claude:conversation:{uuid}",
                 f"- Du {day(c.get('created_at')) or '?'} au {day(c.get('updated_at')) or '?'}, {len(msgs)} messages", ""]
        if c.get("summary"):
            lines += ["## Résumé (Claude.ai)", "", embed(c["summary"]), ""]
        for m in msgs:
            who = "Utilisateur" if m.get("sender") == "human" else "Claude"
            when = (m.get("created_at") or "")[:16].replace("T", " ")
            lines += [f"## {when} · {who}" if when else f"## {who}", "", message_text(m), ""]
        start = day(c.get("created_at"))
        cpath = os.path.join(out, "conversations", f"{start or 'sans-date'}-{slug(name, 50)}-{uuid[:8]}.md")
        with open(cpath, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines).rstrip() + "\n")
        items.append({"cle": f"claude:conversation:{uuid}", "type": "conversation claude", "titre": name,
                      "chemin": cpath, "date": day(c.get("updated_at")) or start, "messages": len(msgs)})

    for f in files["metadata"]:
        items.append({"cle": f"claude:metadonnees:{slug(os.path.basename(f))}", "type": "métadonnées claude",
                      "titre": os.path.basename(f), "chemin": f, "date": "", "exemple": True})
    return items


def walk_files(root, label, dates, exclude=()):
    items = []
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
        for fn in sorted(files):
            p = os.path.join(dirpath, fn)
            if fn.startswith(".") or fn in ("Thumbs.db", "desktop.ini") or p in exclude:
                continue
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            ext = os.path.splitext(fn)[1].lower()
            items.append({"cle": f"{label}:{rel}", "type": TYPES.get(ext, "autre"), "titre": rel, "chemin": p,
                          "date": dates.get(os.path.relpath(p, root)) or day(os.path.getmtime(p))})
    return items


def is_claude_manifest(path):
    if not re.match(r"^manifest-.*\.json$", os.path.basename(path)):
        return False
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            return '"data_files"' in fh.read(4096)
    except OSError:
        return False


CLAUDE_ZIP = re.compile(r"^(conversations|projects|memories|light_metadata|frames)-\d{3}\.zip$")


def claude_parts(source):
    """Archives d'un export Claude.ai par catégories, réunies dans un dossier (manifeste compris ou non)."""
    parts = []
    for dirpath, dirs, files in os.walk(source):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        parts += [os.path.join(dirpath, f) for f in sorted(files) if CLAUDE_ZIP.match(f)]
    return parts


def is_claude_export(root):
    f = claude_files(root)
    return bool(f["conversations"] or f["projects"] or f["memories"])


def write_manifest(path, lot, source, staging, inventory_path, items):
    today = datetime.date.today().isoformat()
    head = ["---", "type: note", "tags: [import]", "---", "",
            f"# Import du lot {lot}", "",
            f"- Source : `{source}`",
            f"- Éléments lus dans : `{staging}`",
            f"- Inventaire détaillé (clé, chemin, empreinte de chaque élément) : `{inventory_path}`",
            f"- Inventaire dressé le {today} par `vault-inventory.py`.", "",
            "Actions : `copier` (fiche ou fichier posé dans le vault), `distiller` (décisions, faits et récit daté "
            "reportés dans une fiche existante), `renvoyer` (lien et contexte, sans copie), `ignorer`. "
            "États : `à décider`, `validé`, `fait`, `ignoré`, `erreur`.", "",
            "## Règles du lot", "",
            "Règles générales qui évitent de trancher ligne par ligne (« tout `Clients/Acme/` vers [[acme]] ») : "
            "à remplir avant validation.", "",
            "## Éléments", "",
            "| n | élément | type | date | action | destination | état |",
            "|---|---|---|---|---|---|---|"]
    rows = []
    for it in items:
        action, etat = "", "à décider"
        if it.get("deja_dans_vault"):
            action, etat = "ignorer", f"déjà dans le vault ({it['deja_dans_vault']})"
        elif it.get("doublon_de"):
            action, etat = "ignorer", f"doublon de {it['doublon_de']}"
        elif it.get("vide"):
            action, etat = "ignorer", "vide"
        elif it.get("exemple"):
            action, etat = "ignorer", "exemple ou métadonnées Claude.ai"
        elif it.get("trop_lourd"):
            action = "renvoyer"
        elif it.get("sensible_probable"):
            action = "renvoyer"
        titre = it["titre"].replace("|", "/")
        if it.get("sensible_probable"):
            titre += " 🔒?"
        rows.append(f"| {it['id']} | {titre} | {it['type']} | {it['date']} | {action} | | {etat} |")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(head + rows) + "\n")


def scan(args):
    source = os.path.realpath(os.path.expanduser(args.source))
    # Sans --vault (entretien d'installation, vault pas encore structuré) : inventaire seul, sans
    # détection des clés déjà importées.
    vault = os.path.realpath(os.path.expanduser(args.vault)) if args.vault else ""
    if vault and not os.path.isdir(os.path.join(vault, "_Meta")):
        sys.exit(f"vault introuvable : {vault} n'a pas de dossier _Meta/")
    if not (os.path.isdir(source) or zipfile.is_zipfile(source)):
        sys.exit(f"source illisible : {source} n'est ni un dossier ni une archive zip")
    if vault and os.path.isdir(source) and (source == vault or source.startswith(vault + os.sep)):
        sys.exit("la source est dans le vault : rien à importer")
    stem = os.path.splitext(os.path.basename(source))[0]
    label = slug(args.label or stem, 40)
    lot = args.lot or f"{datetime.date.today().isoformat()}-{label}"
    staging = os.path.join(state_base(), lot)
    if os.path.isdir(staging):
        shutil.rmtree(staging)
    os.makedirs(staging)

    dates, root = {}, source
    parts = claude_parts(source) if os.path.isdir(source) else []
    if parts:
        # Export Claude.ai par catégories : une archive par catégorie et par partie, extraites côte à côte.
        root = os.path.join(staging, "brut")
        os.makedirs(root)
        for z in parts:
            safe_extract(z, os.path.join(root, os.path.splitext(os.path.basename(z))[0]))
    elif not os.path.isdir(source):
        root = os.path.join(staging, "brut")
        os.makedirs(root)
        dates = safe_extract(source, root)
        # Une archive qui ne contient qu'un dossier : ce dossier est la racine.
        entries = [e for e in os.listdir(root) if not e.startswith(".") and e != "__MACOSX"]
        if len(entries) == 1 and os.path.isdir(os.path.join(root, entries[0])):
            prefix = entries[0]
            root = os.path.join(root, prefix)
            dates = {os.path.relpath(k, prefix): v for k, v in dates.items() if k.startswith(prefix + os.sep)}

    if is_claude_export(root):
        items = split_claude(root, os.path.join(staging, "claude"))
        f = claude_files(root)
        known = set(f["conversations"] + f["projects"] + f["memories"] + f["metadata"])
        items += walk_files(root, label, dates, exclude=known)
    else:
        items = walk_files(root, label, dates)
    # Le manifeste d'un export Claude.ai porte des liens de téléchargement : jamais un élément du lot.
    items = [it for it in items if not is_claude_manifest(it["chemin"])]

    keys = vault_keys(vault) if vault else {}
    seen = {}
    max_bytes = args.max_mb * 1024 * 1024
    for n, it in enumerate(items, 1):
        it["id"] = n
        it["taille"] = os.path.getsize(it["chemin"])
        it["empreinte"] = digest(it["chemin"])
        if it["cle"] in keys:
            it["deja_dans_vault"] = keys[it["cle"]]
        if it["empreinte"] in seen and it["type"] not in ("projet claude",):
            it["doublon_de"] = seen[it["empreinte"]]
        seen.setdefault(it["empreinte"], n)
        if it["taille"] > max_bytes:
            it["trop_lourd"] = True
        if it["taille"] == 0 or it.get("messages") == 0:
            it["vide"] = True
        if SENSIBLE.search(it["titre"]):
            it["sensible_probable"] = True

    inventory_path = os.path.join(staging, "inventaire.json")
    with open(inventory_path, "w", encoding="utf-8") as fh:
        json.dump({"lot": lot, "source": source, "label": label, "racine": root, "elements": items},
                  fh, ensure_ascii=False, indent=1)

    manifest_note = ""
    if args.manifeste:
        mpath = os.path.realpath(os.path.expanduser(args.manifeste))
        if os.path.exists(mpath) and not args.force:
            manifest_note = f"manifeste existant conservé : {mpath} (--force pour le réécrire)"
        else:
            os.makedirs(os.path.dirname(mpath), exist_ok=True)
            write_manifest(mpath, lot, source, root, inventory_path, items)
            manifest_note = f"manifeste : {mpath}"

    by_type = {}
    for it in items:
        by_type[it["type"]] = by_type.get(it["type"], 0) + 1
    summary = {
        "lot": lot, "elements": len(items), "par_type": by_type,
        "deja_dans_vault": sum(1 for i in items if i.get("deja_dans_vault")),
        "doublons": sum(1 for i in items if i.get("doublon_de")),
        "vides": sum(1 for i in items if i.get("vide")),
        "trop_lourds": sum(1 for i in items if i.get("trop_lourd")),
        "sensibles_probables": sum(1 for i in items if i.get("sensible_probable")),
        "export_claude": is_claude_export(root), "inventaire": inventory_path,
    }
    if manifest_note:
        summary["manifeste"] = manifest_note
    print(json.dumps(summary, ensure_ascii=False, indent=1))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan", help="inventorier un dossier ou une archive")
    s.add_argument("source")
    s.add_argument("--vault", help="racine du vault ; sans elle, pas de détection des éléments déjà importés")
    s.add_argument("--label", help="préfixe des clés de fichier ; le garder identique pour relancer un lot")
    s.add_argument("--lot", help="identifiant du lot (défaut : AAAA-MM-JJ-{label})")
    s.add_argument("--manifeste", help="chemin du squelette de manifeste à écrire, dans 00-Inbox/ du vault")
    s.add_argument("--force", action="store_true", help="réécrire un manifeste existant")
    s.add_argument("--max-mb", type=int, default=20, help="taille au-delà de laquelle un élément est signalé")
    args = ap.parse_args()
    if args.cmd == "scan":
        scan(args)


if __name__ == "__main__":
    main()
