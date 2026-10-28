#!/usr/bin/env python3
"""Tests de hooks/vault-inventory.py (inventaire du mode lot de `ranger`).

  python3 dev/tests/test_vault_inventory.py

Chaque test monte un HOME temporaire (vault, sources, état du plugin) et lance le script en sous-processus.
"""
import json, os, subprocess, sys, tempfile, unittest, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPT = os.path.join(ROOT, "hooks", "vault-inventory.py")


def write(path, text=""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


PROJECTS = [{
    "uuid": "p1111111-aaaa", "name": "Refonte site", "description": "Nouveau site vitrine",
    "prompt_template": "Tu es mon assistant pour la refonte.", "created_at": "2026-02-01T09:00:00.000000Z",
    "updated_at": "2026-03-15T10:00:00.000000Z",
    "docs": [{"uuid": "d2222222-bbbb", "filename": "cahier-des-charges.md", "content": "Objectif : 3 pages.",
              "created_at": "2026-02-02T09:00:00.000000Z"}],
}]
CONVERSATIONS = [
    {"uuid": "c3333333-cccc", "name": "Choix du prestataire", "created_at": "2026-02-10T09:00:00.000000Z",
     "updated_at": "2026-02-11T09:00:00.000000Z",
     "chat_messages": [
         {"sender": "human", "text": "On part sur Webflow ?", "created_at": "2026-02-10T09:00:00.000000Z"},
         {"sender": "assistant", "content": [{"type": "text", "text": "Oui, pour trois pages."}],
          "created_at": "2026-02-10T09:01:00.000000Z",
          "attachments": [{"file_name": "devis.txt", "extracted_content": "Devis 4 000 euros"}]}]},
    {"uuid": "c4444444-dddd", "name": "", "created_at": "2026-03-01T09:00:00.000000Z", "chat_messages": []},
]


class Inventory(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = os.path.realpath(self.tmp.name)
        self.vault = os.path.join(self.home, "vault")
        os.makedirs(os.path.join(self.vault, "_Meta"))
        self.env = dict(os.environ, HOME=self.home, XDG_STATE_HOME=os.path.join(self.home, "state"))

    def tearDown(self):
        self.tmp.cleanup()

    def scan(self, source, *extra, check=True, vault=True):
        args = ["--vault", self.vault] if vault else []
        r = subprocess.run([sys.executable, SCRIPT, "scan", source, *args, *extra],
                           env=self.env, capture_output=True, text=True)
        if check:
            self.assertEqual(r.returncode, 0, r.stderr)
            summary = json.loads(r.stdout)
            with open(summary["inventaire"], encoding="utf-8") as fh:
                return summary, json.load(fh)["elements"]
        return r

    def folder(self):
        d = os.path.join(self.home, "Notes")
        write(os.path.join(d, "Clients", "Acme", "kickoff.md"), "# Kickoff\nDécision : lancement en mars.")
        write(os.path.join(d, "Clients", "Acme", "kickoff-copie.md"), "# Kickoff\nDécision : lancement en mars.")
        write(os.path.join(d, "RH", "contrat-dupont.pdf"), "%PDF")
        write(os.path.join(d, "vide.txt"), "")
        write(os.path.join(d, ".DS_Store"), "x")
        write(os.path.join(d, ".git", "config"), "x")
        return d

    def export_zip(self, nested=False):
        z = os.path.join(self.home, "data-2026-10-28.zip")
        prefix = "data-export/" if nested else ""
        with zipfile.ZipFile(z, "w") as zf:
            zf.writestr(prefix + "projects.json", json.dumps(PROJECTS))
            zf.writestr(prefix + "conversations.json", json.dumps(CONVERSATIONS))
            zf.writestr(prefix + "users.json", json.dumps([{"uuid": "u"}]))
        return z

    def test_dossier_lu_en_place_avec_signalements(self):
        summary, items = self.scan(self.folder(), "--label", "notes")
        by = {i["titre"]: i for i in items}
        self.assertEqual(set(by), {"Clients/Acme/kickoff.md", "Clients/Acme/kickoff-copie.md",
                                   "RH/contrat-dupont.pdf", "vide.txt"})
        self.assertEqual(by["Clients/Acme/kickoff.md"]["cle"], "notes:Clients/Acme/kickoff.md")
        pair = [by["Clients/Acme/kickoff.md"], by["Clients/Acme/kickoff-copie.md"]]
        flagged = [i for i in pair if i.get("doublon_de")]
        self.assertEqual(len(flagged), 1)
        self.assertEqual(flagged[0]["doublon_de"], [i for i in pair if i is not flagged[0]][0]["id"])
        self.assertTrue(by["RH/contrat-dupont.pdf"]["sensible_probable"])
        self.assertTrue(by["vide.txt"]["vide"])
        self.assertTrue(by["Clients/Acme/kickoff.md"]["chemin"].startswith(os.path.join(self.home, "Notes")))
        self.assertFalse(summary["export_claude"])

    def test_indice_sensible_sans_faux_positif(self):
        d = os.path.join(self.home, "Docs")
        write(os.path.join(d, "taux-de-redistributivite.md"), "x")
        write(os.path.join(d, "RIB-societe.pdf"), "x")
        _, items = self.scan(d)
        by = {i["titre"]: i for i in items}
        self.assertNotIn("sensible_probable", by["taux-de-redistributivite.md"])
        self.assertTrue(by["RIB-societe.pdf"]["sensible_probable"])

    def test_cle_deja_dans_le_vault(self):
        d = self.folder()
        write(os.path.join(self.vault, "10-Projects", "acme", "kickoff.md"),
              '---\ntype: note\nsource: "notes:Clients/Acme/kickoff.md"\n---\n')
        summary, items = self.scan(d, "--label", "notes")
        hit = [i for i in items if i["titre"] == "Clients/Acme/kickoff.md"][0]
        self.assertEqual(hit["deja_dans_vault"], os.path.join("10-Projects", "acme", "kickoff.md"))
        self.assertEqual(summary["deja_dans_vault"], 1)

    def test_export_claude_decoupe_hors_vault(self):
        summary, items = self.scan(self.export_zip())
        self.assertTrue(summary["export_claude"])
        types = sorted(i["type"] for i in items)
        self.assertEqual(types, ["conversation claude", "conversation claude", "document claude",
                                 "métadonnées claude", "projet claude"])
        state = os.path.join(self.home, "state", "second-cerveau", "import")
        for i in items:
            self.assertTrue(i["chemin"].startswith(state), i["chemin"])
            self.assertFalse(i["chemin"].startswith(self.vault))
        projet = [i for i in items if i["type"] == "projet claude"][0]
        self.assertEqual(projet["cle"], "claude:projet:p1111111-aaaa")
        text = open(projet["chemin"], encoding="utf-8").read()
        self.assertIn("## Instructions du projet", text)
        self.assertIn("cahier-des-charges.md", text)
        conv = [i for i in items if i["cle"] == "claude:conversation:c3333333-cccc"][0]
        self.assertEqual(conv["date"], "2026-02-11")
        ctext = open(conv["chemin"], encoding="utf-8").read()
        self.assertIn("Oui, pour trois pages.", ctext)
        self.assertIn("Devis 4 000 euros", ctext)
        vide = [i for i in items if i["cle"] == "claude:conversation:c4444444-dddd"][0]
        self.assertTrue(vide["vide"])

    def export_par_categories(self):
        """Disposition réelle constatée le 2026-10-28 : un manifeste et une archive par catégorie."""
        d = os.path.join(self.home, "claude-export")
        os.makedirs(d)
        write(os.path.join(d, "manifest-abc-2026-10-28.json"), json.dumps(
            {"version": "1.0", "data_files": [{"category": "projects", "export_url": "https://claude.ai/export/x"}]}))
        with zipfile.ZipFile(os.path.join(d, "projects-000.zip"), "w") as zf:
            for p in PROJECTS + [{"uuid": "p5555555-eeee", "name": "How to use Claude", "is_starter_project": True, "docs": []}]:
                zf.writestr(f"projects/{p['uuid']}.json", json.dumps(p))
        conv = dict(CONVERSATIONS[0], summary="Choix de Webflow pour le site.")
        conv["chat_messages"] = [dict(conv["chat_messages"][1], content=[
            {"type": "thinking", "thinking": "réflexion interne"}, {"type": "text", "text": "Oui, pour trois pages."},
            {"type": "tool_use", "name": "web_search", "input": {}}])]
        os.makedirs(os.path.join(d, "conversations-000"))
        with zipfile.ZipFile(os.path.join(d, "conversations-000", "conversations-000.zip"), "w") as zf:
            zf.writestr("conversations.json", json.dumps([conv]))
        with zipfile.ZipFile(os.path.join(d, "memories-000.zip"), "w") as zf:
            zf.writestr("memories/m1.json", json.dumps({
                "conversations_memory": "Lucas dirige devlc.", "account_uuid": "acc",
                "project_memories": {"p1111111-aaaa": "Refonte : maquette validée le 10/03."},
                "memory_files": [{"path": "/projects/p1111111-aaaa/index.md", "content": "Index refonte\n\n## État\n\nMaquette validée", "updated_at": "2026-03-10T00:00:00Z"},
                                 {"path": "/people/flore.md", "content": "Flore, associée", "updated_at": "2026-03-01T00:00:00Z"}]}))
        with zipfile.ZipFile(os.path.join(d, "light_metadata-000.zip"), "w") as zf:
            zf.writestr("users.json", "[]")
            zf.writestr("login_history.json", "[]")
        return d

    def test_export_par_categories(self):
        m = os.path.join(self.vault, "00-Inbox", "import-claude.md")
        summary, items = self.scan(self.export_par_categories(), "--label", "claude", "--manifeste", m)
        self.assertTrue(summary["export_claude"])
        by = {i["cle"]: i for i in items}
        self.assertNotIn("manifest", " ".join(i["titre"] for i in items))
        projet = by["claude:projet:p1111111-aaaa"]
        self.assertTrue(projet["memoire"])
        ptext = open(projet["chemin"], encoding="utf-8").read()
        self.assertIn("## Mémoire du projet (Claude.ai)", ptext)
        self.assertIn("Index refonte", ptext)
        self.assertTrue(by["claude:projet:p5555555-eeee"]["exemple"])
        self.assertEqual(by["claude:memoire:generale"]["type"], "mémoire claude")
        self.assertIn("claude:memoire:people-flore-md", by)
        self.assertNotIn("claude:memoire:projects-p1111111-aaaa-index-md", by)
        ctext = open(by["claude:conversation:c3333333-cccc"]["chemin"], encoding="utf-8").read()
        self.assertIn("## Résumé (Claude.ai)", ctext)
        self.assertIn("Outil utilisé : web_search", ctext)
        self.assertNotIn("réflexion interne", ctext)
        self.assertIn("#### État", ptext)
        self.assertNotIn("\n## État", ptext)
        self.assertEqual(sum(1 for i in items if i["type"] == "métadonnées claude"), 2)
        text = open(m, encoding="utf-8").read()
        self.assertIn("exemple ou métadonnées Claude.ai", text)
        self.assertNotIn("claude.ai/export", text)

    def test_memoire_citee_reconnue(self):
        write(os.path.join(self.vault, "20-Areas", "equipe", "flore.md"),
              "---\ntype: note\n---\n- associée (source : claude:memoire:people-flore-md)\n")
        _, items = self.scan(self.export_par_categories(), "--label", "claude")
        hit = [i for i in items if i["cle"] == "claude:memoire:people-flore-md"][0]
        self.assertEqual(hit["deja_dans_vault"], os.path.join("20-Areas", "equipe", "flore.md"))

    def test_sans_vault_pour_l_entretien(self):
        # À l'entretien d'installation, le dossier n'a pas encore de _Meta/ : inventaire seul.
        write(os.path.join(self.vault, "10-Projects", "site", "site.md"),
              "---\ntype: project\n---\n- (source : claude:conversation:c3333333-cccc)\n")
        dossier = os.path.join(self.home, "futur-vault")
        os.makedirs(dossier)
        m = os.path.join(dossier, "00-Inbox", "import-claude.md")
        summary, items = self.scan(self.export_par_categories(), "--label", "claude", "--manifeste", m, vault=False)
        self.assertTrue(summary["export_claude"])
        self.assertEqual(summary["deja_dans_vault"], 0)
        self.assertTrue(os.path.isfile(m))
        self.assertIn("claude:memoire:generale", {i["cle"] for i in items})

    def test_archive_a_dossier_unique(self):
        summary, items = self.scan(self.export_zip(nested=True))
        self.assertTrue(summary["export_claude"])

    def test_cle_claude_citee_dans_un_journal(self):
        write(os.path.join(self.vault, "10-Projects", "site", "site.md"),
              "---\ntype: project\n---\n## Journal\n- 2026-02-11 · Webflow retenu (source : claude:conversation:c3333333-cccc)\n")
        summary, items = self.scan(self.export_zip())
        conv = [i for i in items if i["cle"] == "claude:conversation:c3333333-cccc"][0]
        self.assertEqual(conv["deja_dans_vault"], os.path.join("10-Projects", "site", "site.md"))

    def test_manifeste_squelette_et_conservation(self):
        m = os.path.join(self.vault, "00-Inbox", "import-notes.md")
        self.scan(self.folder(), "--label", "notes", "--manifeste", m)
        text = open(m, encoding="utf-8").read()
        self.assertIn("type: note", text)
        self.assertIn("| n | élément | type | date | action | destination | état |", text)
        self.assertIn("RH/contrat-dupont.pdf 🔒? | pdf |", text)
        self.assertIn("| renvoyer |", text)
        self.assertRegex(text, r"\| ignorer \| \| doublon de \d+ \|")
        write(m, "modifié à la main")
        summary, _ = self.scan(self.folder(), "--label", "notes", "--manifeste", m)
        self.assertIn("conservé", summary["manifeste"])
        self.assertEqual(open(m, encoding="utf-8").read(), "modifié à la main")

    def test_zip_slip_refuse(self):
        z = os.path.join(self.home, "piege.zip")
        with zipfile.ZipFile(z, "w") as zf:
            zf.writestr("../../evil.md", "x")
            zf.writestr("ok.md", "# ok")
        summary, items = self.scan(z)
        self.assertEqual([i["titre"] for i in items], ["ok.md"])
        self.assertFalse(os.path.exists(os.path.join(self.home, "evil.md")))

    def test_source_dans_le_vault_refusee(self):
        r = self.scan(self.vault, check=False)
        self.assertNotEqual(r.returncode, 0)

    def test_relance_meme_lot_stable(self):
        d = self.folder()
        _, a = self.scan(d, "--label", "notes", "--lot", "l1")
        _, b = self.scan(d, "--label", "notes", "--lot", "l1")
        self.assertEqual([i["cle"] for i in a], [i["cle"] for i in b])


if __name__ == "__main__":
    unittest.main(verbosity=2)
