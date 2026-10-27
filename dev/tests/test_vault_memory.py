#!/usr/bin/env python3
"""Tests de hooks/vault-memory.py (état de la mémoire native) et de son signalement par vault-health.sh.

  python3 dev/tests/test_vault_memory.py

Chaque test monte un HOME temporaire (dossiers mémoire, vault, réglages) et lance le script en sous-processus.
Dépendances : python3, git, bash.
"""
import sys
sys.dont_write_bytecode = True
import hashlib, importlib.util, json, os, re, subprocess, tempfile, time, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPT = os.path.join(ROOT, "hooks", "vault-memory.py")
HEALTH = os.path.join(ROOT, "hooks", "vault-health.sh")
_spec = importlib.util.spec_from_file_location("vault_memory", SCRIPT)
vm = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(vm)


def tree_hash(root):
    h = hashlib.sha256()
    for r, dirs, files in sorted(os.walk(root)):
        dirs.sort()
        for fn in sorted(files):
            p = os.path.join(r, fn)
            h.update(p.encode())
            if os.path.isfile(p) and not os.path.islink(p):
                with open(p, "rb") as fh:
                    h.update(fh.read())
    return h.hexdigest()


def memory(name, body, typ="project"):
    return f"---\nname: {name}\ndescription: {name}\nmetadata:\n  type: {typ}\n---\n\n{body}\n"


def sanitize(path):
    return re.sub(r"[^a-zA-Z0-9]", "-", path)


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = os.path.realpath(self.tmp.name)
        self.vault = os.path.join(self.home, "vault")
        for d in ("_Meta", "10-Projects/alpha", "20-Areas/rh", "20-Areas/ventes", "40-Archive/projects/vieux",
                  "30-Resources/img"):
            os.makedirs(os.path.join(self.vault, d))
        self.write(os.path.join(self.vault, "_Meta", "hooks.conf"), "MEMORY_MAX_LINES=10\nMEMORY_MAX_KB=2\n")
        self.write(os.path.join(self.vault, "10-Projects/alpha/alpha.md"), "---\ntype: project\n---\n# alpha\n")
        self.write(os.path.join(self.vault, "10-Projects/alpha/_index.md"), "# index\n")
        self.write(os.path.join(self.vault, "20-Areas/ventes/_index.md"), "# index\n")
        self.write(os.path.join(self.vault, "30-Resources/img/schema.png"), "png")
        self.write(os.path.join(self.vault, "40-Archive/projects/vieux/vieux.md"), "---\ntype: project\n---\n# vieux\n")
        self.write(os.path.join(self.vault, "20-Areas/rh/salaires-equipe.md"),
                   '---\ntype: note\nsensibilité: "confidentiel"\n---\n# Salaires\n')
        self.write(os.path.join(self.vault, "20-Areas/rh/budget.md"), "---\ntype: note\nconfidentiel: true\n---\n# B\n")
        self.env = dict(os.environ, HOME=self.home, XDG_STATE_HOME=os.path.join(self.home, "state"),
                        GIT_CONFIG_NOSYSTEM="1", PYTHONDONTWRITEBYTECODE="1")
        for k in ("CLAUDE_PROJECT_DIR", "CLAUDE_CONFIG_DIR"):
            self.env.pop(k, None)
        self.mem = self.memdir(self.vault)

    def tearDown(self):
        for r, dirs, files in os.walk(self.home):
            for x in dirs + files:
                try:
                    os.chmod(os.path.join(r, x), 0o700)
                except OSError:
                    pass
        self.tmp.cleanup()

    def write(self, path, text):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)

    def memdir(self, workdir, config=None):
        d = os.path.join(config or os.path.join(self.home, ".claude"), "projects", sanitize(workdir), "memory")
        os.makedirs(d, exist_ok=True)
        return d

    def put(self, d, files, index=None):
        for name, text in files.items():
            self.write(os.path.join(d, name), text)
        lines = index if index is not None else [f"- [{n}]({n}) — accroche" for n in files]
        self.write(os.path.join(d, "MEMORY.md"), "\n".join(lines) + "\n")

    def run_cli(self, *args, cwd=None, ok=True, env=None):
        r = subprocess.run([sys.executable, SCRIPT, *args], env=env or self.env, capture_output=True, text=True,
                           cwd=cwd or self.home)
        if ok:
            self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout if ok else r

    def check(self, d=None):
        return json.loads(self.run_cli("check", "--vault", self.vault, d or self.mem))

    def git(self, cwd, *a):
        subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "init.defaultBranch=main", *a],
                       cwd=cwd, env=self.env, check=True, capture_output=True)


class Emplacement(Base):
    def where(self, d, env=None):
        return json.loads(self.run_cli("where", d, env=env))

    def test_racine_git_sous_dossier_et_worktree(self):
        self.git(self.vault, "init", "-q")
        self.git(self.vault, "commit", "-q", "--allow-empty", "-m", "i")
        self.assertEqual(self.where(os.path.join(self.vault, "10-Projects", "alpha"))["dir"], self.mem)
        wt = os.path.join(self.home, "wt")
        self.git(self.vault, "worktree", "add", "-q", wt)
        self.assertEqual(self.where(wt)["dir"], self.mem)

    def test_sous_module_reste_a_sa_propre_racine(self):
        sub = os.path.join(self.home, "lib"); os.makedirs(sub)
        self.git(sub, "init", "-q"); self.git(sub, "commit", "-q", "--allow-empty", "-m", "i")
        sup = os.path.join(self.home, "repo"); os.makedirs(sup)
        self.git(sup, "init", "-q"); self.git(sup, "commit", "-q", "--allow-empty", "-m", "i")
        self.git(sup, "-c", "protocol.file.allow=always", "submodule", "add", "-q", sub, "mods/sub")
        out = self.where(os.path.join(sup, "mods", "sub"))
        self.assertTrue(out["dir"].endswith(sanitize(os.path.join(sup, "mods", "sub")) + "/memory"), out)

    def test_claude_config_dir_et_chemin_long_et_emoji(self):
        cfg = os.path.join(self.home, "autre-config")
        env = dict(self.env, CLAUDE_CONFIG_DIR=cfg)
        self.assertTrue(self.where(self.vault, env)["dir"].startswith(os.path.join(cfg, "projects")))
        self.assertEqual(vm.sanitize("/x" * 150)[-7:], "-4y6yx2")        # empreinte vérifiée avec Node
        self.assertEqual(vm.sanitize("/a/🔒 x"), "-a----x")              # emoji : deux unités UTF-16

    def test_auto_memory_directory_ordre_et_valeurs(self):
        cible = os.path.join(self.vault, "_Meta", "memoire")
        self.write(os.path.join(self.home, ".claude", "settings.json"), json.dumps({"autoMemoryDirectory": "~/mem-user"}))
        out = self.where(self.vault)
        self.assertEqual((out["dir"], out["source"]), (os.path.join(self.home, "mem-user"), "utilisateur"))
        self.write(os.path.join(self.vault, ".claude", "settings.json"), json.dumps({"autoMemoryDirectory": "/projet"}))
        self.assertEqual(self.where(self.vault)["source"], "projet")   # lu si le dossier est de confiance
        self.write(os.path.join(self.vault, ".claude", "settings.local.json"), json.dumps({"autoMemoryDirectory": cible}))
        self.assertEqual(self.where(self.vault), {"dir": cible, "source": "local", "exists": False})
        for bad in ("mem-relatif", "~", ""):
            self.write(os.path.join(self.vault, ".claude", "settings.local.json"), json.dumps({"autoMemoryDirectory": bad}))
            out = self.where(self.vault)
            self.assertEqual(out["dir"], self.mem, bad)                 # valeur rejetée : défaut, sans source suivante
            self.assertIn("valeur rejetée", out["source"])
        for junk in ("[]", "null", "{pas du json"):
            self.write(os.path.join(self.vault, ".claude", "settings.local.json"), junk)
            self.assertEqual(self.where(self.vault)["source"], "projet")


class Inventaire(Base):
    def test_part_du_plafond_et_repetitions_entre_dossiers(self):
        regle = memory("demander-avant-ecrire", "Toujours demander avant d'écrire dans un outil externe, "
                       "Notion, Airtable, Gmail : jamais d'écriture sans validation explicite de Lucas.", "feedback")
        self.put(self.mem, {"a.md": memory("a", "x"), "regle.md": regle})
        d2 = self.memdir(os.path.join(self.home, "projects", "repo"))
        self.put(d2, {"regle-bis.md": regle.replace("Toujours", "Il faut toujours")}, index=["- [r](regle-bis.md) — x"] * 180)
        d3 = self.memdir(os.path.join(self.home, "projects", "gros"))
        self.put(d3, {"b.md": memory("b", "y")}, index=["- [b](b.md) — " + "x" * 130] * 210)
        user_dir = os.path.join(self.home, "mem-user")
        self.put(user_dir, {"u.md": memory("u", "z")})
        self.write(os.path.join(self.home, ".claude", "settings.json"), json.dumps({"autoMemoryDirectory": user_dir}))
        out = json.loads(self.run_cli("inventory", "--vault", self.vault))
        pct = {x["dir"]: x["cap_pct"] for x in out["dirs"]}
        self.assertGreater(pct[d3], 100)
        self.assertEqual(pct[d2], 90)
        self.assertEqual(out["hard_cap"], {"lines": 200, "chars": 25000})
        self.assertEqual(len(out["cross_repeats"]), 1)
        self.assertEqual([x["dir"] for x in out["dirs"]].count(user_dir), 1)

    def test_dossier_illisible(self):
        self.put(self.mem, {"a.md": memory("a", "x"), "b.md": memory("b", "y")})
        os.chmod(os.path.join(self.mem, "b.md"), 0)
        r = self.check()
        self.assertEqual(r["unreadable"], ["b.md"])
        self.assertEqual(r["index"]["missing_files"], [])
        d2 = self.memdir(os.path.join(self.home, "projects", "ferme"))
        self.put(d2, {"c.md": memory("c", "z")})
        os.chmod(d2, 0)
        out = json.loads(self.run_cli("inventory", "--vault", self.vault))
        self.assertIn("(dossier illisible)", [u for x in out["dirs"] for u in x["unreadable"]])


class Controle(Base):
    def test_budget_alerte_et_troncature_en_caracteres(self):
        self.put(self.mem, {f"m{k}.md": memory(f"m{k}", "texte") for k in range(12)})
        r = self.check()
        self.assertTrue(r["over_budget"]); self.assertFalse(r["alert"]); self.assertFalse(r["truncated"])
        line = "- [é](e.md) — " + "é" * 140                  # 154 lignes, ~23 000 caractères, ~45 000 octets
        self.write(os.path.join(self.mem, "MEMORY.md"), "\n".join([line] * 154) + "\n")
        r = self.check()
        self.assertTrue(r["alert"]); self.assertFalse(r["truncated"])
        self.write(os.path.join(self.mem, "MEMORY.md"), "\n".join(["- x"] * 201) + "\n")
        self.assertTrue(self.check()["truncated"])

    def test_pointeurs(self):
        body = ("Voir [[alpha]], [[Alpha]], [[alpha.md]], [[10-Projects/alpha/alpha]], [[alpha\\|A]], ![[schema.png]], "
                "[[vieux]], [[disparu]], [[autre-memoire]].\n"
                "Chemins : 10-Projects/alpha/alpha.md#Statut, 10-Projects/alpha/alpha, **10-Projects/alpha/alpha.md**, "
                "~/vault/10-Projects/beta/alpha.md, 20-Areas/x/vieux.md, 30-Resources/rien.md, "
                "20-Areas/autre/_index.md, _Meta/hooks.conf, _personas/cos, gabarit 10-Projects/{slug}/{slug}.md, 00-Inbox/r/AAAA-MM-JJ.md, _Meta/….")
        os.symlink(self.vault, os.path.join(self.home, "vault-lien"))
        os.makedirs(os.path.join(self.vault, "_personas", "cos"))
        self.put(self.mem, {"p.md": memory("p", body), "autre_memoire.md": memory("autre", "z")})
        got = {(x["kind"], x["pointer"]) for x in self.check()["pointers"]}
        self.assertEqual(got, {("archivé", "[[vieux]]"), ("cassé", "[[disparu]]"),
                               ("déplacé", "10-Projects/beta/alpha.md"), ("archivé", "20-Areas/x/vieux.md"),
                               ("cassé", "30-Resources/rien.md"), ("ambigu", "20-Areas/autre/_index.md")})

    def test_aucune_fuite_par_les_pointeurs(self):
        body = "[[ ouverte sans fermeture.\nmot de passe : Hunter2Hunter2!\nFin ]\n10-Projects/x/password=SuperSecret123"
        self.put(self.mem, {"f.md": memory("f", body)})
        out = self.run_cli("check", "--vault", self.vault, self.mem)
        for leak in ("Hunter2", "SuperSecret"):
            self.assertNotIn(leak, out)

    def test_sensible_detecte(self):
        cases = [
            "Clé : sk-ant-" + "a1B2" * 8, "postgres://user:hunter2@db.example.com/prod",
            "-----BEGIN OPENSSH PRIVATE KEY-----", "sk_live_" + "a" * 24, "glpat-" + "b" * 20, "gho_" + "c" * 30,
            "ntn_" + "d" * 30, "secret_" + "e" * 40, "pat" + "A" * 14 + "." + "f" * 40,
            "https://hooks.slack.com/services/T000/B000/XXXXXXXXXXXX", "aws_secret_access_key = abcdEFGH1234ijkl",
            "OPENAI_API_KEY=abcdEFGH1234", "STRIPE_SECRET_KEY=abcdEFGH1234", "DB_PASSWORD=p4ss.word9",
            "mdp : Azerty2026!", "Mot de passe du NAS : Bonjour2026", "Authorization: Bearer abcdefghij0123456789",
            "IBAN fr76 3000 6000 0112 3456 7890 189", "IBAN FR76-3000-6000-0112-3456-7890-189",
            "Appeler le 06 12 34 56 78", "Tél. +33 (0)6 12 34 56 78", "Voir [[salaires-equipe]].",
            "Le dossier salaires-equipe est à jour.", "Voir [[budget]].",
        ]
        self.put(self.mem, {"s.md": memory("s", "\n".join(cases))})
        r = self.check()
        lines = {x["line"] for x in r["sensitive"]}
        first = 8                                            # le corps commence à la ligne 8 du fichier
        missed = [c for k, c in enumerate(cases) if first + k not in lines]
        self.assertEqual(missed, [])
        self.assertEqual({tuple(sorted(x)) for x in r["sensitive"]}, {("file", "kind", "line")})   # rien d'autre
        self.assertNotIn("salaires", json.dumps(r))                      # ni le nom d'une fiche confidentielle

    def test_sensible_faux_positifs(self):
        cases = ["Version 0.13.2, commit 5425874, ticket IZU-78.", "Le budget de la refonte est validé.",
                 "headers: {'Secret': input.config.secret}", "`POSTGRES_PASSWORD/POSTGRES_DB=railway`",
                 "`ONYX_API_KEY`, `N8N_API_KEY`, mots de passe) : `setup.sh`",
                 "Réunion le 05-12-2026 14:30.", "Commande n° 0612345678 livrée.", "Réf. AB12CDEF3456GHIJ7890",
                 "token: 1234567890123 tokens", "password: /run/secrets/db", "api-key: xkeysib-...",
                 "TOKEN=$(railway whoami)", "X-N8N-API-KEY: $N8N_KEY"]
        self.put(self.mem, {"s.md": memory("s", "\n".join(cases))})
        self.assertEqual(self.check()["sensitive"], [])

    def test_doublons_et_index(self):
        txt = "Le client préfère des comptes rendus courts, envoyés le vendredi, avec les décisions en tête."
        self.put(self.mem, {"a.md": memory("a", txt), "b.md": memory("b", txt + " Toujours."),
                            "c d.md": memory("c", "Sans rapport : configuration du serveur de fichiers."),
                            "e.md": memory("e", "autre sujet de configuration réseau")},
                 index=["- [a](a.md#détail) — x", "- [b](b.md \"titre\") — x", "- [c](<c d.md>) — x",
                        "- [fiche](~/vault/10-Projects/alpha/alpha.md) — x", "- [fantome](fantome.md) — x"])
        r = self.check()
        self.assertEqual([(d["a"], d["b"]) for d in r["duplicates"]], [("a.md", "b.md")])
        self.assertEqual(r["index"], {"missing_files": ["fantome.md"], "unindexed": ["e.md"]})

    def test_curation_due_et_sauvegarde(self):
        self.put(self.mem, {"a.md": memory("a", "x")})
        os.symlink(os.path.join(self.home, "inexistant"), os.path.join(self.mem, "lien-casse"))
        self.assertTrue(self.check()["curation_due"])
        h = tree_hash(self.mem)
        out = json.loads(self.run_cli("backup", self.mem))
        self.assertTrue(out["backup"].startswith(os.path.join(self.home, "state", "second-cerveau", "memoire")))
        self.assertEqual(sorted(os.listdir(out["backup"])), [".source", "MEMORY.md", "a.md", "lien-casse"])
        self.assertEqual(h, tree_hash(self.mem))
        self.assertFalse(self.check()["curation_due"])
        out2 = json.loads(self.run_cli("backup", self.mem))              # deux sauvegardes dans la même seconde
        self.assertNotEqual(out["backup"], out2["backup"])
        os.makedirs(os.path.join(self.home, "state", "second-cerveau", "memoire", "avant-migration-x"))
        self.check()                                                     # dossier d'état mal nommé : pas de plantage

    def test_curation_due_apres_le_delai(self):
        self.put(self.mem, {"a.md": memory("a", "x")})
        old = time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time() - 40 * 86400)) + "-000000-" + vm.fingerprint(self.mem)
        os.makedirs(os.path.join(self.home, "state", "second-cerveau", "memoire", old))
        self.assertTrue(self.check()["curation_due"])

    def test_sauvegardes_de_deux_dossiers_proches_distinctes(self):
        a = self.memdir(os.path.join(self.home, "clientA", "x" * 90))
        b = self.memdir(os.path.join(self.home, "clientB", "x" * 90))
        self.put(a, {"a.md": memory("a", "x")}); self.put(b, {"b.md": memory("b", "y")})
        self.run_cli("backup", a)
        self.assertTrue(self.check(b)["curation_due"])

    def test_backup_refuse_un_dossier_quelconque(self):
        r = self.run_cli("backup", self.home, ok=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse(os.path.isdir(os.path.join(self.home, "state", "second-cerveau", "memoire")) and
                         [x for x in os.listdir(os.path.join(self.home, "state", "second-cerveau", "memoire"))
                          if not x.startswith(".")])

    def test_lecture_seule(self):
        self.put(self.mem, {"a.md": memory("a", "[[disparu]] 06 12 34 56 78")})
        h, hp = tree_hash(self.home), tree_hash(os.path.join(ROOT, "hooks"))
        self.run_cli("check", "--vault", self.vault, self.mem)
        self.run_cli("inventory", "--vault", self.vault)
        self.run_cli("where", self.vault)
        self.assertEqual(h, tree_hash(self.home))
        self.assertEqual(hp, tree_hash(os.path.join(ROOT, "hooks")))    # pas de __pycache__ dans le plugin

    def test_non_utf8_et_index_absent(self):
        with open(os.path.join(self.mem, "a.md"), "wb") as fh:
            fh.write(b"\xff\xfe binaire")
        r = self.check()
        self.assertEqual(r["index_lines"], 0)
        self.assertEqual(r["index"]["unindexed"], ["a.md"])

    def test_performance_avec_beaucoup_de_fiches_confidentielles(self):
        for k in range(700):
            self.write(os.path.join(self.vault, "20-Areas/rh", f"dossier-confidentiel-{k}.md"),
                       "---\ntype: note\nconfidentiel: true\n---\n# x\n")
        self.put(self.mem, {f"m{k}.md": memory(f"m{k}", "ligne ordinaire\n" * 30) for k in range(20)})
        t = time.time()
        self.check()
        self.assertLess(time.time() - t, 5)


class Signalement(Base):
    def health(self, cwd=None, env=None):
        out = subprocess.run(["bash", HEALTH], input=json.dumps({"cwd": cwd or self.vault}), env=env or self.env,
                             capture_output=True, text=True).stdout
        return json.loads(out)["hookSpecificOutput"]["additionalContext"] if out.strip() else ""

    def test_vault_health(self):
        self.put(self.mem, {"a.md": memory("a", "x")})
        self.assertNotIn("Mémoire native", self.health())
        self.put(self.mem, {f"m{k}.md": memory(f"m{k}", "x") for k in range(12)})
        self.assertIn("Mémoire native : index de 12 lignes", self.health())
        self.put(self.mem, {"s.md": memory("s", "Appeler le 06 12 34 56 78")}, index=["- [s](s.md) — x"])
        self.assertIn("1 mémoire(s) au contenu sensible apparent", self.health())

    def test_tronque_meme_avec_un_budget_au_dessus_du_plafond(self):
        self.write(os.path.join(self.vault, "_Meta", "hooks.conf"), "MEMORY_MAX_LINES=500\nMEMORY_MAX_KB=100\n")
        self.write(os.path.join(self.mem, "MEMORY.md"), "\n".join(["- x"] * 250) + "\n")
        self.assertIn("index tronqué au chargement", self.health())

    def test_hors_vault_et_script_en_echec(self):
        ailleurs = os.path.join(self.home, "ailleurs"); os.makedirs(ailleurs)
        self.assertEqual(self.health(cwd=ailleurs), "")
        self.write(os.path.join(self.vault, ".claude", "settings.local.json"), "null")
        self.put(self.mem, {f"m{k}.md": memory(f"m{k}", "x") for k in range(12)})
        self.assertIn("Mémoire native", self.health())


class SecondePasse(Base):
    """Cas issus de la seconde revue."""

    def test_caractere_unicode_replie_ne_fait_pas_planter(self):
        self.put(self.mem, {f"m{k}.md": memory(f"m{k}", "AB12 3456 7890 12\u212a4 et \u0130BAN") for k in range(12)})
        self.check()
        out = subprocess.run(["bash", HEALTH], input=json.dumps({"cwd": self.vault}), env=self.env,
                             capture_output=True, text=True).stdout
        self.assertIn("Mémoire native : index de 12 lignes", out)

    def test_prose_avec_mot_cle_n_est_pas_un_secret(self):
        cases = ["Le token GitHub : renouvelé tous les 90 jours", "Le mot de passe : demander à Jean-Baptiste",
                 "password: obligatoire", "Le secret de la réussite : persévérance",
                 "Pour le token, voir la doc : https://docs.github.com/fr/authentication",
                 "Réinitialiser le mot de passe : https://accounts.google.com/signin",
                 "api_key: ANTHROPIC_API_KEY dans .env", "access_key: AWS_ACCESS_KEY_ID",
                 "client_secret: CLIENT_SECRET_FROM_VAULT", "token: documentation.md", "token: expires_in=3600"]
        self.put(self.mem, {"p.md": memory("p", "\n".join(cases))})
        self.assertEqual(self.check()["sensitive"], [])

    def test_telephone_apres_un_prenom_en_id(self):
        self.put(self.mem, {"t.md": memory("t", "Contact : David 06 12 34 56 78\nAstrid : 06 12 34 56 78")})
        self.assertEqual(len(self.check()["sensitive"]), 2)

    def test_reglages_de_projet_lus_dans_le_dossier_de_lancement_seulement(self):
        self.git(self.vault, "init", "-q")
        persona = os.path.join(self.vault, "_personas", "cos"); os.makedirs(persona)
        self.write(os.path.join(self.vault, ".claude", "settings.json"), json.dumps({"autoMemoryDirectory": "~/via-projet"}))
        out = json.loads(self.run_cli("where", persona))
        self.assertEqual(out["dir"], self.mem)                         # pas lu depuis un sous-dossier
        self.assertEqual(json.loads(self.run_cli("where", self.vault))["source"], "projet")
        self.write(os.path.join(self.vault, ".claude", "settings.local.json"), json.dumps({"autoMemoryDirectory": "~/via-local"}))
        out = json.loads(self.run_cli("where", persona))
        self.assertEqual((out["dir"], out["source"]), (os.path.join(self.home, "via-local"), "local"))
        self.write(os.path.join(self.vault, ".claude", "settings.local.json"), json.dumps({"autoMemoryDirectory": "  ~/espace  "}))
        self.assertIn("valeur rejetée", json.loads(self.run_cli("where", persona))["source"])

    def test_code_inline_et_blocs(self):
        body = ("Convention : `[[nom-du-client]]` et `10-Projects/nom-projet/nom-projet.md`.\n"
                "```\n[[exemple]] 10-Projects/exemple/exemple.md\n```\n")
        self.put(self.mem, {"c.md": memory("c", body)})
        self.run_cli("backup", self.mem)
        r = self.check()
        self.assertEqual([(p["pointer"], p.get("code")) for p in r["pointers"]],
                         [("10-Projects/nom-projet/nom-projet.md", True)])
        self.assertFalse(r["needs_curation"])

    def test_fiche_nommee_en_nfd(self):
        import unicodedata
        d = os.path.join(self.vault, "20-Areas", unicodedata.normalize("NFD", "équipe"))
        self.write(os.path.join(d, unicodedata.normalize("NFD", "réunion.md")), "# r\n")
        self.put(self.mem, {"n.md": memory("n", "Voir 20-Areas/équipe/réunion.md et [[réunion]].")})
        self.assertEqual(self.check()["pointers"], [])

    def test_index_point_slash(self):
        self.put(self.mem, {"b.md": memory("b", "x")}, index=["- [b](./b.md) — x"])
        self.assertEqual(self.check()["index"], {"missing_files": [], "unindexed": []})

    def test_nom_de_fichier_non_utf8(self):
        self.put(self.mem, {"a.md": memory("a", "x")})
        with open(os.path.join(self.mem.encode(), b"caf\xe9.md"), "wb") as fh:
            fh.write(b"x")
        r = self.check()
        self.assertIn("caf\ufffd.md", r["index"]["unindexed"])

    def test_dossier_illisible_signale_au_bilan(self):
        self.put(self.mem, {"a.md": memory("a", "x")})
        os.chmod(self.mem, 0)
        out = subprocess.run(["bash", HEALTH], input=json.dumps({"cwd": self.vault}), env=self.env,
                             capture_output=True, text=True).stdout
        self.assertIn("illisible", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
