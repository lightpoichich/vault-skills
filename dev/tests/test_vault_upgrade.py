#!/usr/bin/env python3
"""Tests de hooks/vault-upgrade.py (mise à niveau d'un vault installé) et de son signal dans vault-health.sh.

  python3 dev/tests/test_vault_upgrade.py

Chaque test copie le plugin (hooks, gabarits d'installation, manifeste) dans un dossier temporaire, pour
pouvoir faire évoluer un gabarit, monte un vault installé à partir de ces gabarits et lance les scripts en
sous-processus.
"""
import importlib.util, json, os, re, shutil, subprocess, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def write(path, text=""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = os.path.realpath(self.tmp.name)
        self.plugin = os.path.join(self.home, "plugin")
        shutil.copytree(os.path.join(ROOT, "hooks"), os.path.join(self.plugin, "hooks"),
                        ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(os.path.join(ROOT, "skills", "installer", "assets"),
                        os.path.join(self.plugin, "skills", "installer", "assets"))
        shutil.copytree(os.path.join(ROOT, ".claude-plugin"), os.path.join(self.plugin, ".claude-plugin"))
        self.assets = os.path.join(self.plugin, "skills", "installer", "assets")
        self.script = os.path.join(self.plugin, "hooks", "vault-upgrade.py")
        self.vault = os.path.join(self.home, "vault")
        self.env = dict(os.environ, HOME=self.home, XDG_STATE_HOME=os.path.join(self.home, "state"))
        self.env.pop("CLAUDE_PROJECT_DIR", None)

    def tearDown(self):
        self.tmp.cleanup()

    def install(self, stamp=True):
        """Pose ce que la phase de structure copie ou génère, gabarits tels quels."""
        cos = os.path.join(self.assets, "persona-chief-of-staff")
        shutil.copytree(cos, os.path.join(self.vault, "_personas", "cos"))
        os.makedirs(os.path.join(self.vault, "_Meta"), exist_ok=True)
        shutil.copy(os.path.join(self.assets, "hooks", "hooks.conf"), os.path.join(self.vault, "_Meta", "hooks.conf"))
        shutil.copy(os.path.join(self.assets, "vault-claude-template.md"), os.path.join(self.vault, "CLAUDE.md"))
        shutil.copy(os.path.join(self.assets, "schema-template.md"), os.path.join(self.vault, "_Meta", "Schema.md"))
        if stamp:
            self.run_cmd("stamp", "--apply")

    def run_cmd(self, *args, check=True):
        r = subprocess.run([sys.executable, self.script, args[0], "--vault", self.vault, *args[1:]],
                           env=self.env, capture_output=True, text=True)
        if check:
            self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout

    def check(self):
        out = json.loads(self.run_cmd("check"))
        return out, {u["unite"]: u["cas"] for u in out["unites"]}

    def brief(self):
        return os.path.join(self.vault, "_personas", "cos", ".claude", "skills", "brief-du-jour", "SKILL.md")

    def brief_template(self):
        return os.path.join(self.assets, "persona-chief-of-staff", ".claude", "skills", "brief-du-jour", "SKILL.md")

    def append(self, path, text):
        write(path, read(path) + text)


class Cases(Base):
    BRIEF = "_personas/cos/.claude/skills/brief-du-jour/SKILL.md"

    def test_installation_fraiche_a_jour(self):
        self.install()
        out, cases = self.check()
        self.assertTrue(out["tampon"])
        self.assertEqual(set(cases.values()), {"a-jour"})
        self.assertIn("_personas/cos/CLAUDE.md#regles", cases)
        self.assertIn("CLAUDE.md#carte", cases)
        self.assertIn("_Meta/Schema.md#conventions", cases)
        self.assertNotIn("_personas/cos/capacites-a-construire.md", cases)
        self.assertFalse(out["a_faire"])
        self.assertEqual(self.run_cmd("check", "--summary"), "")
        stamp = read(os.path.join(self.vault, "_Meta", "installation.md"))
        self.assertIn("type: moc", stamp)
        self.assertIn("5.0.0-noms-skills", stamp)

    def test_remplacable_puis_remplace(self):
        self.install()
        self.append(self.brief_template(), "\nNouvelle consigne du plugin.\n")
        _, cases = self.check()
        self.assertEqual(cases[self.BRIEF], "remplacable")
        self.assertIn("mise à niveau disponible", self.run_cmd("check", "--summary"))
        plan = json.loads(self.run_cmd("apply", "--apply"))
        self.assertEqual(read(self.brief()), read(self.brief_template()))
        self.assertTrue(os.path.isdir(plan["sauvegarde"]))
        _, cases = self.check()
        self.assertEqual(cases[self.BRIEF], "a-jour")

    def test_personnalise_gabarit_inchange(self):
        self.install()
        self.append(self.brief(), "\nMa règle à moi.\n")
        _, cases = self.check()
        self.assertEqual(cases[self.BRIEF], "personnalise")
        before = read(self.brief())
        self.run_cmd("apply", "--apply")
        self.assertEqual(read(self.brief()), before)

    def test_fusion_jamais_ecrite_puis_acceptee(self):
        self.install()
        self.append(self.brief(), "\nMa règle à moi.\n")
        self.append(self.brief_template(), "\nNouvelle consigne du plugin.\n")
        _, cases = self.check()
        self.assertEqual(cases[self.BRIEF], "fusion")
        before = read(self.brief())
        plan = json.loads(self.run_cmd("apply", "--apply"))
        self.assertEqual(read(self.brief()), before)
        self.assertIn(self.BRIEF, [x["unite"] for x in plan["a_revoir"]])
        self.run_cmd("accept", "--apply", self.BRIEF)
        _, cases = self.check()
        self.assertEqual(cases[self.BRIEF], "personnalise")
        self.assertEqual(self.run_cmd("check", "--summary"), "")

    def test_bloc_remplace_texte_hors_bloc_intact(self):
        self.install()
        claude = os.path.join(self.vault, "CLAUDE.md")
        write(claude, read(claude).replace("## Ton (comment t'adresser)", "## Ton (comment t'adresser)\n\nMa note perso."))
        tpl = os.path.join(self.assets, "vault-claude-template.md")
        write(tpl, read(tpl).replace("Ce sont des rappels", "Ce sont seulement des rappels"))
        _, cases = self.check()
        self.assertEqual(cases["CLAUDE.md#regles"], "remplacable")
        self.assertEqual(cases["CLAUDE.md#carte"], "a-jour")
        self.run_cmd("apply", "--apply")
        text = read(claude)
        self.assertIn("Ce sont seulement des rappels", text)
        self.assertIn("Ma note perso.", text)
        self.assertEqual(text.count("<!-- socle second-cerveau : début regles -->"), 1)

    def test_bloc_personnalise_et_fusion(self):
        self.install()
        cos = os.path.join(self.vault, "_personas", "cos", "CLAUDE.md")
        write(cos, read(cos).replace("- Supprimer une fiche sans validation explicite.",
                                     "- Supprimer une fiche sans validation explicite.\n- Écrire en anglais."))
        _, cases = self.check()
        self.assertEqual(cases["_personas/cos/CLAUDE.md#regles"], "personnalise")
        tpl = os.path.join(self.assets, "persona-chief-of-staff", "CLAUDE.md")
        write(tpl, read(tpl).replace("Inventer du contenu", "Inventer un contenu"))
        _, cases = self.check()
        self.assertEqual(cases["_personas/cos/CLAUDE.md#regles"], "fusion")
        before = read(cos)
        self.run_cmd("apply", "--apply")
        self.assertEqual(read(cos), before)

    def test_balises_absentes(self):
        self.install()
        cos = os.path.join(self.vault, "_personas", "cos", "CLAUDE.md")
        write(cos, re.sub(r"<!-- socle second-cerveau : (début|fin) regles -->\n?", "", read(cos)))
        _, cases = self.check()
        self.assertEqual(cases["_personas/cos/CLAUDE.md#regles"], "balises-absentes")
        before = read(cos)
        self.run_cmd("apply", "--apply")
        self.assertEqual(read(cos), before)
        self.assertEqual(self.run_cmd("check", "--summary"), "")

    def test_nouveau_fichier_du_gabarit(self):
        self.install()
        new = os.path.join(self.assets, "persona-chief-of-staff", ".claude", "skills", "brief-du-jour",
                           "references", "nouvelle.md")
        write(new, "# Nouvelle référence\n")
        key = "_personas/cos/.claude/skills/brief-du-jour/references/nouvelle.md"
        _, cases = self.check()
        self.assertEqual(cases[key], "nouveau")
        self.run_cmd("apply", "--apply")
        self.assertTrue(os.path.isfile(os.path.join(self.vault, key)))

    def test_pas_de_brief_orphelin_sans_chief_of_staff(self):
        self.install()
        shutil.rmtree(os.path.join(self.vault, "_personas", "cos"))
        write(os.path.join(self.assets, "persona-chief-of-staff", ".claude", "skills", "brief-du-jour",
                           "references", "nouvelle.md"), "# Nouvelle\n")
        _, cases = self.check()
        self.assertEqual(cases["_personas/cos/.claude/skills/brief-du-jour/references/nouvelle.md"], "absent")
        self.run_cmd("apply", "--apply")
        self.assertFalse(os.path.exists(os.path.join(self.vault, "_personas", "cos")))

    def test_simulation_n_ecrit_rien(self):
        self.install()
        stamp = read(os.path.join(self.vault, "_Meta", "installation.md"))
        self.append(self.brief_template(), "\nNouvelle consigne.\n")
        before = read(self.brief())
        plan = json.loads(self.run_cmd("apply"))
        self.assertFalse(plan["ecrit"])
        self.assertTrue(plan["plan"])
        self.assertEqual(read(self.brief()), before)
        self.assertEqual(read(os.path.join(self.vault, "_Meta", "installation.md")), stamp)


class SansTampon(Base):
    def test_premiere_mise_a_niveau_n_ecrase_rien(self):
        self.install(stamp=False)
        self.append(self.brief(), "\nBrief réécrit par l'utilisateur.\n")
        self.assertIn("ne connaît pas encore les fichiers", self.run_cmd("check", "--summary"))
        out, cases = self.check()
        self.assertFalse(out["tampon"])
        self.assertEqual(cases["_personas/cos/.claude/skills/brief-du-jour/SKILL.md"], "inconnu")
        self.assertEqual(cases["_Meta/hooks.conf"], "a-jour")
        before = read(self.brief())
        self.run_cmd("apply", "--apply")
        self.assertEqual(read(self.brief()), before)
        stamp = read(os.path.join(self.vault, "_Meta", "installation.md"))
        data = json.loads(re.search(r"```json\n(.*?)\n```", stamp, re.S).group(1))
        self.assertIsNone(data["unites"]["_personas/cos/.claude/skills/brief-du-jour/SKILL.md"]["empreinte"])
        self.assertTrue(data["unites"]["_Meta/hooks.conf"]["empreinte"])
        self.assertEqual(self.run_cmd("check", "--summary"), "")
        # Le gabarit change ensuite : l'unité sans empreinte reste à revoir, jamais remplacée d'office.
        self.append(self.brief_template(), "\nNouvelle consigne.\n")
        self.run_cmd("apply", "--apply")
        self.assertEqual(read(self.brief()), before)


class Migrations(Base):
    def setup_old_names(self):
        self.install(stamp=False)
        root = os.path.join(self.vault, "CLAUDE.md")
        self.append(root, "\n`import-note` fait entrer une note ; import-note sans accents reste tel quel.\n")
        skill = os.path.join(self.vault, "_personas", "commercial", ".claude", "skills", "kickstart-client", "SKILL.md")
        write(skill, "Déléguer à `nouveau-projet`.\nVoir aussi `kickstart-vault`.\n")
        write(os.path.join(self.vault, "_personas", "commercial", "CLAUDE.md"), "C'est le rôle de `kickstart-persona`.\n")
        ref = os.path.join(self.vault, "_personas", "cos", ".claude", "skills", "brief-du-jour", "references", "format-brief.md")
        self.append(ref, "\nRéponse traitée par `nouveau-projet`.\n")
        os.symlink("../../../commercial/.claude/skills/kickstart-client",
                   os.path.join(self.vault, "_personas", "cos", ".claude", "skills", "kickstart-client"))
        fiche = os.path.join(self.vault, "10-Projects", "x", "x.md")
        write(fiche, "Historique : on utilisait `nouveau-projet`.\n")
        return root, skill, ref, fiche

    def test_migration_noms_puis_idempotence(self):
        root, skill, ref, fiche = self.setup_old_names()
        out, _ = self.check()
        mig = [m for m in out["migrations_en_attente"] if m["id"] == "5.0.0-noms-skills"][0]
        files = sorted(o["fichier"] for o in mig["occurrences"])
        self.assertIn("_personas/commercial/.claude/skills/kickstart-client/SKILL.md", files)
        self.assertEqual(len([f for f in files if f.endswith("kickstart-client/SKILL.md")]), 1)
        self.run_cmd("apply", "--apply")
        self.assertEqual(read(skill), "Déléguer à `structurer`.\nVoir aussi `/second-cerveau:installer`.\n")
        self.assertIn("`ranger` fait entrer une note ; import-note sans accents reste tel quel.", read(root))
        self.assertIn("`assistants`", read(os.path.join(self.vault, "_personas", "commercial", "CLAUDE.md")))
        self.assertIn("`structurer`", read(ref))
        self.assertIn("`nouveau-projet`", read(fiche))
        out, _ = self.check()
        self.assertEqual(out["migrations_en_attente"], [])
        plan = json.loads(self.run_cmd("apply", "--apply"))
        self.assertEqual(plan["plan"], [])

    def test_table_concorde_avec_audit(self):
        spec = importlib.util.spec_from_file_location("vault_upgrade", self.script)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        checks = read(os.path.join(ROOT, "skills", "audit-vault", "references", "checks.md"))
        table = dict(re.findall(r"^\| `([a-z-]+)` \| [\d.]+ \| `([^`]+)`", checks, re.M))
        self.assertEqual(table, mod.RETIRED)


class Health(Base):
    def health(self):
        hook = os.path.join(self.plugin, "hooks", "vault-health.sh")
        out = subprocess.run(["bash", hook], input=json.dumps({"cwd": self.vault}), env=self.env,
                             capture_output=True, text=True).stdout
        return json.loads(out)["hookSpecificOutput"]["additionalContext"] if out.strip() else ""

    def test_signal_tampon_absent_puis_silence(self):
        self.install(stamp=False)
        self.assertIn("ne connaît pas encore les fichiers", self.health())
        self.run_cmd("apply", "--apply")
        self.assertNotIn("mise à niveau", self.health())
        self.assertNotIn("ne connaît pas encore", self.health())

    def test_signal_mise_a_niveau_et_coupure(self):
        self.install()
        self.append(self.brief_template(), "\nNouvelle consigne.\n")
        self.assertIn("mise à niveau disponible", self.health())
        self.append(os.path.join(self.vault, "_Meta", "hooks.conf"), "\nUPGRADE_REMINDER=0\n")
        self.assertNotIn("mise à niveau", self.health())


if __name__ == "__main__":
    unittest.main(verbosity=2)
