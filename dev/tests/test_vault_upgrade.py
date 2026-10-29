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

    def conf(self):
        return os.path.join(self.vault, "_Meta", "hooks.conf")

    def conf_template(self):
        return os.path.join(self.assets, "hooks", "hooks.conf")

    def brief(self):
        return os.path.join(self.vault, "_personas", "cos", ".claude", "skills", "brief-du-jour", "SKILL.md")

    def brief_template(self):
        return os.path.join(self.assets, "persona-chief-of-staff", ".claude", "skills", "brief-du-jour", "SKILL.md")

    def stamp_data(self):
        stamp = read(os.path.join(self.vault, "_Meta", "installation.md"))
        return json.loads(re.search(r"```json\n(.*?)\n```", stamp, re.S).group(1))

    def append(self, path, text):
        write(path, read(path) + text)


class Cases(Base):
    CONF = "_Meta/hooks.conf"

    def test_installation_fraiche_a_jour(self):
        self.install()
        out, cases = self.check()
        self.assertTrue(out["tampon"])
        self.assertEqual(set(cases.values()), {"a-jour"})
        self.assertEqual(set(cases), {self.CONF, "CLAUDE.md#carte", "CLAUDE.md#regles", "_Meta/Schema.md#conventions"})
        self.assertFalse(out["a_faire"])
        self.assertEqual(self.run_cmd("check", "--summary"), "")
        stamp = read(os.path.join(self.vault, "_Meta", "installation.md"))
        self.assertIn("type: moc", stamp)
        self.assertIn("5.0.0-noms-skills", stamp)

    def test_remplacable_puis_remplace(self):
        self.install()
        self.append(self.conf_template(), "\n# Nouveau réglage documenté.\n")
        _, cases = self.check()
        self.assertEqual(cases[self.CONF], "remplacable")
        self.assertIn("mise à niveau disponible", self.run_cmd("check", "--summary"))
        plan = json.loads(self.run_cmd("apply", "--apply"))
        self.assertEqual(read(self.conf()), read(self.conf_template()))
        self.assertTrue(os.path.isdir(plan["sauvegarde"]))
        _, cases = self.check()
        self.assertEqual(cases[self.CONF], "a-jour")

    def test_personnalise_gabarit_inchange(self):
        self.install()
        self.append(self.conf(), "\nEXCLUDE=outillage\n")
        _, cases = self.check()
        self.assertEqual(cases[self.CONF], "personnalise")
        before = read(self.conf())
        self.run_cmd("apply", "--apply")
        self.assertEqual(read(self.conf()), before)

    def test_fusion_jamais_ecrite_puis_acceptee(self):
        self.install()
        self.append(self.conf(), "\nEXCLUDE=outillage\n")
        self.append(self.conf_template(), "\n# Nouveau réglage documenté.\n")
        _, cases = self.check()
        self.assertEqual(cases[self.CONF], "fusion")
        before = read(self.conf())
        plan = json.loads(self.run_cmd("apply", "--apply"))
        self.assertEqual(read(self.conf()), before)
        self.assertIn(self.CONF, [x["unite"] for x in plan["a_revoir"]])
        self.run_cmd("accept", "--apply", self.CONF)
        _, cases = self.check()
        self.assertEqual(cases[self.CONF], "personnalise")
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
        claude = os.path.join(self.vault, "CLAUDE.md")
        write(claude, read(claude).replace("Ce sont des rappels", "Ce sont des rappels discrets"))
        _, cases = self.check()
        self.assertEqual(cases["CLAUDE.md#regles"], "personnalise")
        tpl = os.path.join(self.assets, "vault-claude-template.md")
        write(tpl, read(tpl).replace("pas des blocages", "jamais des blocages"))
        _, cases = self.check()
        self.assertEqual(cases["CLAUDE.md#regles"], "fusion")
        before = read(claude)
        self.run_cmd("apply", "--apply")
        self.assertEqual(read(claude), before)

    def test_balises_absentes(self):
        self.install()
        schema = os.path.join(self.vault, "_Meta", "Schema.md")
        write(schema, re.sub(r"<!-- socle second-cerveau : (début|fin) conventions -->\n?", "", read(schema)))
        _, cases = self.check()
        self.assertEqual(cases["_Meta/Schema.md#conventions"], "balises-absentes")
        before = read(schema)
        self.run_cmd("apply", "--apply")
        self.assertEqual(read(schema), before)
        self.assertEqual(self.run_cmd("check", "--summary"), "")

    def test_persona_et_brief_non_geres(self):
        self.install()
        self.append(self.brief_template(), "\nNouvelle consigne du plugin.\n")
        tpl = os.path.join(self.assets, "persona-chief-of-staff", "CLAUDE.md")
        self.append(tpl, "\n- Nouvelle règle du plugin.\n")
        before = read(self.brief())
        out, cases = self.check()
        self.assertFalse([k for k in cases if k.startswith("_personas/")])
        self.assertFalse(out["a_faire"])
        self.assertEqual(self.run_cmd("check", "--summary"), "")
        self.run_cmd("apply", "--apply")
        self.assertEqual(read(self.brief()), before)

    def test_empreintes_heritees_retirees_sans_signal(self):
        self.install()
        path = os.path.join(self.vault, "_Meta", "installation.md")
        data = self.stamp_data()
        data["unites"]["_personas/cos/CLAUDE.md#regles"] = {"mode": "bloc", "empreinte": "0123456789abcdef"}
        data["unites"]["_personas/cos/.claude/skills/brief-du-jour/SKILL.md"] = {"mode": "copie", "empreinte": None}
        text = read(path)
        write(path, re.sub(r"```json\n.*?\n```", lambda m: "```json\n" + json.dumps(data) + "\n```", text, flags=re.S))
        out, cases = self.check()
        self.assertNotIn("retire", cases.values())
        self.assertFalse(out["a_faire"])
        self.assertEqual(self.run_cmd("check", "--summary"), "")
        self.append(self.conf_template(), "\n# Nouveau réglage documenté.\n")
        self.run_cmd("apply", "--apply")
        self.assertFalse([k for k in self.stamp_data()["unites"] if k.startswith("_personas/")])

    def test_hooks_conf_supprime_reste_absent(self):
        self.install()
        os.remove(self.conf())
        _, cases = self.check()
        self.assertEqual(cases[self.CONF], "absent")
        self.run_cmd("apply", "--apply")
        self.assertFalse(os.path.exists(self.conf()))

    def test_simulation_n_ecrit_rien(self):
        self.install()
        stamp = read(os.path.join(self.vault, "_Meta", "installation.md"))
        self.append(self.conf_template(), "\n# Nouveau réglage documenté.\n")
        before = read(self.conf())
        plan = json.loads(self.run_cmd("apply"))
        self.assertFalse(plan["ecrit"])
        self.assertTrue(plan["plan"])
        self.assertEqual(read(self.conf()), before)
        self.assertEqual(read(os.path.join(self.vault, "_Meta", "installation.md")), stamp)


class SansTampon(Base):
    def test_premiere_mise_a_niveau_n_ecrase_rien(self):
        self.install(stamp=False)
        schema = os.path.join(self.vault, "_Meta", "Schema.md")
        write(schema, read(schema).replace("<!-- socle second-cerveau : début conventions -->\n",
                                           "<!-- socle second-cerveau : début conventions -->\nMa convention.\n"))
        self.assertIn("ne connaît pas encore les fichiers", self.run_cmd("check", "--summary"))
        out, cases = self.check()
        self.assertFalse(out["tampon"])
        self.assertEqual(cases["_Meta/Schema.md#conventions"], "inconnu")
        self.assertEqual(cases["_Meta/hooks.conf"], "a-jour")
        before = read(schema)
        self.run_cmd("apply", "--apply")
        self.assertEqual(read(schema), before)
        data = self.stamp_data()
        self.assertIsNone(data["unites"]["_Meta/Schema.md#conventions"]["empreinte"])
        self.assertTrue(data["unites"]["_Meta/hooks.conf"]["empreinte"])
        self.assertEqual(self.run_cmd("check", "--summary"), "")
        # Le gabarit change ensuite : l'unité sans empreinte reste à revoir, jamais remplacée d'office.
        tpl = os.path.join(self.assets, "schema-template.md")
        write(tpl, read(tpl).replace("<!-- socle second-cerveau : fin conventions -->",
                                     "Nouvelle convention.\n<!-- socle second-cerveau : fin conventions -->"))
        self.run_cmd("apply", "--apply")
        self.assertEqual(read(schema), before)

    def test_hooks_conf_jamais_pose_est_ajoute(self):
        self.install(stamp=False)
        os.remove(self.conf())
        _, cases = self.check()
        self.assertEqual(cases["_Meta/hooks.conf"], "nouveau")
        plan = json.loads(self.run_cmd("apply"))
        step = [x for x in plan["plan"] if x.get("unite") == "_Meta/hooks.conf"][0]
        self.assertEqual(step["action"], "ajouté")
        self.assertIn("JOURNAL_ROTATION=1", step["effet"])
        self.run_cmd("apply", "--apply")
        self.assertEqual(read(self.conf()), read(self.conf_template()))
        _, cases = self.check()
        self.assertEqual(cases["_Meta/hooks.conf"], "a-jour")

    def test_hooks_conf_absent_apres_une_mise_a_niveau_5_2(self):
        """Fiche d'installation posée par la 5.2.x alors que hooks.conf manquait : empreinte nulle, donc ajout."""
        self.install(stamp=False)
        os.remove(self.conf())
        data = {"version": "5.2.5", "migrations": ["5.0.0-noms-skills"],
                "unites": {"_Meta/hooks.conf": {"mode": "copie", "empreinte": None}}}
        write(os.path.join(self.vault, "_Meta", "installation.md"), "```json\n" + json.dumps(data) + "\n```\n")
        _, cases = self.check()
        self.assertEqual(cases["_Meta/hooks.conf"], "nouveau")
        self.assertIn("mise à niveau disponible", self.run_cmd("check", "--summary"))

    def test_ajout_refuse_par_accept(self):
        self.install(stamp=False)
        os.remove(self.conf())
        self.run_cmd("accept", "--apply", "_Meta/hooks.conf")
        _, cases = self.check()
        self.assertEqual(cases["_Meta/hooks.conf"], "absent")
        self.run_cmd("apply", "--apply")
        self.assertFalse(os.path.exists(self.conf()))


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

    LEGACY = {
        "permissions": {"allow": ["Bash(git status)"]},
        "autoMemoryEnabled": True,
        "hooks": {
            "SessionStart": [{"hooks": [{"type": "command",
                                          "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/vault-health.sh",
                                          "statusMessage": "Bilan de sante du vault..."}]}],
            "PostToolUse": [{"matcher": "Write|Edit|MultiEdit",
                             "hooks": [{"type": "command",
                                        "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/vault-note-guard.sh"}]}],
            "Stop": [{"hooks": [{"type": "command", "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/vault-git-sync.sh"}]}],
        },
    }

    def setup_local_hooks(self, settings=None):
        self.install(stamp=False)
        claude = os.path.join(self.vault, ".claude")
        write(os.path.join(claude, "settings.json"),
              settings if settings is not None else json.dumps(self.LEGACY, indent=2) + "\n")
        for name in ("vault-health.sh", "vault-note-guard.sh", "vault-git-sync.sh"):
            write(os.path.join(claude, "hooks", name), "#!/bin/bash\n")
        return claude

    def test_migration_hooks_locaux(self):
        claude = self.setup_local_hooks()
        out, _ = self.check()
        mig = [m for m in out["migrations_en_attente"] if m["id"] == "5.3.0-hooks-locaux"][0]
        files = sorted(o["fichier"] for o in mig["occurrences"])
        self.assertEqual(files, [".claude/hooks/vault-health.sh", ".claude/hooks/vault-note-guard.sh",
                                 ".claude/settings.json"])
        before = read(os.path.join(claude, "settings.json"))
        self.run_cmd("apply")
        self.assertEqual(read(os.path.join(claude, "settings.json")), before)
        plan = json.loads(self.run_cmd("apply", "--apply"))
        data = json.loads(read(os.path.join(claude, "settings.json")))
        self.assertEqual(data["permissions"], self.LEGACY["permissions"])
        self.assertTrue(data["autoMemoryEnabled"])
        self.assertEqual(set(data["hooks"]), {"Stop"})
        self.assertFalse(os.path.exists(os.path.join(claude, "hooks", "vault-health.sh")))
        self.assertFalse(os.path.exists(os.path.join(claude, "hooks", "vault-note-guard.sh")))
        self.assertTrue(os.path.isfile(os.path.join(claude, "hooks", "vault-git-sync.sh")))
        saved = os.path.join(plan["sauvegarde"], ".claude")
        self.assertTrue(os.path.isfile(os.path.join(saved, "hooks", "vault-health.sh")))
        self.assertEqual(read(os.path.join(saved, "settings.json")), before)
        out, _ = self.check()
        self.assertEqual(out["migrations_en_attente"], [])
        self.assertEqual(self.run_cmd("check", "--summary"), "")

    def test_hooks_locaux_seuls_dossier_retire(self):
        legacy = dict(self.LEGACY, hooks={k: v for k, v in self.LEGACY["hooks"].items() if k != "Stop"})
        claude = self.setup_local_hooks(json.dumps(legacy))
        os.remove(os.path.join(claude, "hooks", "vault-git-sync.sh"))
        self.run_cmd("apply", "--apply")
        data = json.loads(read(os.path.join(claude, "settings.json")))
        self.assertNotIn("hooks", data)
        self.assertFalse(os.path.exists(os.path.join(claude, "hooks")))

    def test_hooks_locaux_encore_appeles_gardes(self):
        claude = self.setup_local_hooks()
        write(os.path.join(claude, "settings.local.json"),
              json.dumps({"hooks": {"SessionStart": [{"hooks": [{"type": "command",
                         "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/vault-health.sh"}]}]}}))
        self.run_cmd("apply", "--apply")
        self.assertTrue(os.path.isfile(os.path.join(claude, "hooks", "vault-health.sh")))
        self.assertFalse(os.path.exists(os.path.join(claude, "hooks", "vault-note-guard.sh")))

    def test_hooks_locaux_json_illisible_intact(self):
        claude = self.setup_local_hooks('{"hooks": // commentaire\n}')
        before = read(os.path.join(claude, "settings.json"))
        self.run_cmd("apply", "--apply")
        self.assertEqual(read(os.path.join(claude, "settings.json")), before)
        self.assertTrue(os.path.isfile(os.path.join(claude, "hooks", "vault-health.sh")))

    def test_installation_fraiche_migrations_faites(self):
        self.install()
        self.assertIn("5.3.0-hooks-locaux", read(os.path.join(self.vault, "_Meta", "installation.md")))

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
        tpl = os.path.join(self.assets, "vault-claude-template.md")
        write(tpl, read(tpl).replace("Ce sont des rappels", "Ce sont seulement des rappels"))
        self.assertIn("mise à niveau disponible", self.health())
        self.append(os.path.join(self.vault, "_Meta", "hooks.conf"), "\nUPGRADE_REMINDER=0\n")
        self.assertNotIn("mise à niveau", self.health())


if __name__ == "__main__":
    unittest.main(verbosity=2)
