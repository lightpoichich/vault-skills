#!/usr/bin/env python3
"""Tests de hooks/vault-journal.py (rotation des journaux de fiche) et de son signalement par vault-health.sh.

  python3 dev/tests/test_vault_journal.py

Chaque test monte un vault temporaire. Toute rotation écrite est suivie d'un contrôle de non-perte : chaque ligne
non vide d'avant se retrouve, à l'identique, dans la fiche ou ses journaux. Dépendances : python3, git, bash.
"""
import sys
sys.dont_write_bytecode = True
import hashlib, importlib.util, json, os, subprocess, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPT = os.path.join(ROOT, "hooks", "vault-journal.py")
HEALTH = os.path.join(ROOT, "hooks", "vault-health.sh")
_spec = importlib.util.spec_from_file_location("vault_journal", SCRIPT)
vj = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(vj)

PAD = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore. " * 12


def fiche(title="alpha", typ="project", updated="2026-10-27", journal="", before="", after="", nl="\n"):
    text = (f"---\ntype: {typ}\nstatus: active\nupdated: {updated}\n---\n\n# {title}\n\n## Suivi\n\nÉtat courant.\n\n"
            f"{before}## Journal\n\n{journal}\n## Décisions\n\n- **2026-01-01 — Décision en vigueur.** Raison.\n{after}")
    return text.replace("\n", nl)


def entries(dates, fmt="- **{d} : entrée.** {pad}", sub=0):
    out = []
    for d in dates:
        out.append(fmt.format(d=d, pad=PAD))
        out += [f"  - détail {k} de {d} : {PAD[:200]}" for k in range(sub)]
    return "\n".join(out) + "\n"


def read(path, binary=False):
    with open(path, "rb") as fh:
        data = fh.read()
    return data if binary else data.decode("utf-8")


def tree_hash(root):
    h = hashlib.sha256()
    for r, dirs, files in sorted(os.walk(root)):
        dirs.sort()
        for fn in sorted(files):
            p = os.path.join(r, fn)
            h.update(p.encode()); h.update(read(p, binary=True))
    return h.hexdigest()


class Base(unittest.TestCase):
    conf = "JOURNAL_ROTATION=1\nJOURNAL_MAX_KB_PROJECT=4\nJOURNAL_KEEP=2\n"

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = os.path.realpath(self.tmp.name)
        self.vault = os.path.join(self.root, "vault")
        os.makedirs(os.path.join(self.vault, "_Meta"))
        self.write(os.path.join(self.vault, "_Meta", "hooks.conf"), self.conf)
        self.env = dict(os.environ, HOME=self.root, XDG_STATE_HOME=os.path.join(self.root, "state"),
                        GIT_CONFIG_NOSYSTEM="1")
        self.env.pop("CLAUDE_PROJECT_DIR", None)
        os.environ["XDG_STATE_HOME"] = self.env["XDG_STATE_HOME"]

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, path, text, binary=False):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(text if binary else text.encode("utf-8"))

    def sheet(self, text, slug="alpha"):
        p = os.path.join(self.vault, "10-Projects", slug, f"{slug}.md")
        self.write(p, text)
        return p

    def run_cli(self, *args):
        r = subprocess.run([sys.executable, SCRIPT, *args], env=self.env, capture_output=True, text=True)
        return r.returncode, r.stdout

    def rotate(self, path, apply=True):
        code, out = self.run_cli("rotate", *(["--apply"] if apply else []), path)
        return code, json.loads(out)[0]

    def journals(self, path):
        d = os.path.join(os.path.dirname(path), "journal")
        return sorted(os.path.join(d, f) for f in os.listdir(d)) if os.path.isdir(d) else []

    def assertNoLoss(self, before, path):
        after = [read(path)] + [read(j) for j in self.journals(path)]
        self.assertEqual(vj.missing_lines([before], after), [])


class Rotation(Base):
    def test_puces_iso_en_un_paragraphe(self):
        dates = ["2026-10-20", "2026-10-02", "2026-09-15", "2026-09-03", "2026-08-30", "2026-07-01", "2026-06-29"]
        before = fiche(journal=entries(dates))
        p = self.sheet(before)
        code, r = self.rotate(p)
        self.assertEqual(code, 0, r)
        self.assertLessEqual(os.path.getsize(p), 4 * 1024)
        names = [os.path.basename(j) for j in self.journals(p)]
        self.assertIn("alpha-2026-T2.md", names)
        self.assertIn("alpha-2026-T3.md", names)
        text = read(p)
        self.assertIn("2026-10-20", text)                       # la plus récente reste
        self.assertNotIn("2026-06-29", text.split("## Journaux")[0])
        self.assertIn("- [[alpha-2026-T3]]", text)
        self.assertIn("## Décisions", text)
        self.assertNoLoss(before, p)
        t2 = read(self.journals(p)[0])
        self.assertIn("type: journal", t2)
        self.assertIn('source: "[[alpha]]"', t2)

    def test_sous_puces_et_tiret_dans_le_titre(self):
        dates = ["2026-10-20", "2026-10-10", "2026-09-01", "2026-08-01"]
        before = fiche(journal=entries(dates, fmt="- **{d} — Lot livré.** {pad}", sub=3))
        p = self.sheet(before)
        self.rotate(p)
        j = read(self.journals(p)[0])
        self.assertIn("- **2026-08-01 — Lot livré.** " + PAD + "\n  - détail 0 de 2026-08-01", j)
        self.assertIn("détail 2 de 2026-08-01", j)
        self.assertNotIn("détail 0 de 2026-08-01", read(p))
        self.assertNoLoss(before, p)

    def test_dates_sans_annee_ou_hors_tete_epinglees(self):
        pinned = ["- **Rapports qualité du 20/01 au 26/01 : stable.** " + PAD,
                  "- **Lot 1/3 livré.** " + PAD,
                  "- **Sprint 3/4 : livré le 2026-01-09.** " + PAD,
                  "- **Retour sur la décision du 2025-01-10 (20/10).** " + PAD,
                  "- **12/10 : point d'étape.** " + PAD]
        journal = entries(["2026-10-25", "2026-10-20"]) + "\n".join(pinned) + "\n" + entries(
            ["01/06/2026", "2026-05-01", "2026-04-01"])
        before = fiche(journal=journal)
        p = self.sheet(before)
        code, r = self.rotate(p)
        self.assertEqual(code, 0, r)
        self.assertTrue(any("épinglées" in w for w in r["warnings"]), r)
        text = read(p)
        for ln in pinned:
            self.assertIn(ln, text)                          # aucune entrée sans date sûre ne bouge
        self.assertNotIn("2026-04-01", text.split("## Journaux")[0])
        self.assertIn("alpha-2026-T2.md", [os.path.basename(j) for j in self.journals(p)])
        self.assertNoLoss(before, p)

    def test_date_jj_mm_aaaa_en_tete(self):
        self.assertEqual(vj.head_date("- **01/06/2026 : x**"), vj.dt.date(2026, 6, 1))
        self.assertEqual(vj.head_date("- [x] 2026-06-01 fait"), vj.dt.date(2026, 6, 1))
        self.assertEqual(vj.head_date("### **2026-06-01 — Réunion**"), vj.dt.date(2026, 6, 1))
        self.assertIsNone(vj.head_date("- **0000-01-01 : an zéro**"))
        self.assertIsNone(vj.head_date("- **24/7 : astreinte**"))
        self.assertIsNone(vj.head_date("- **Sprint 3/4 : livré le 2026-09-01**"))

    def test_blocs_h3_ordre_ancien_d_abord(self):
        blocs = "".join(f"### {d} — Réunion\n\n{PAD}\n\n- point A\n- point B\n\n" for d in
                        ["2026-03-01", "2026-04-01", "2026-07-01", "2026-09-01", "2026-10-01"])
        before = fiche(journal=blocs)
        p = self.sheet(before)
        code, r = self.rotate(p)
        self.assertEqual(code, 0, r)
        text = read(p)
        self.assertNotIn("### 2026-03-01", text)
        self.assertIn("### 2026-10-01", text)
        j = read([x for x in self.journals(p) if x.endswith("T1.md")][0])
        self.assertIn("### 2026-03-01 — Réunion", j)
        self.assertIn("- point B", j)
        self.assertNoLoss(before, p)

    def test_entree_sans_date_epinglee(self):
        journal = entries(["2026-10-20", "2026-10-01"]) + f"- **Point sans date.** {PAD}\n" + entries(
            ["2026-07-01", "2026-06-01", "2026-05-01"])
        before = fiche(journal=journal)
        p = self.sheet(before)
        code, r = self.rotate(p)
        self.assertTrue(any("épinglées" in w for w in r["warnings"]))
        self.assertIn("Point sans date", read(p))
        self.assertNotIn("2026-05-01", read(p).split("## Journaux")[0])
        self.assertNoLoss(before, p)

    def test_date_complete_hors_ordre_deplacee_selon_sa_date(self):
        journal = entries(["2026-10-20", "2026-10-10", "2026-05-01", "2026-09-01", "2026-08-01"])
        before = fiche(journal=journal)
        p = self.sheet(before)
        self.rotate(p)
        self.assertNotIn("2026-05-01", read(p).split("## Journaux")[0])
        self.assertNoLoss(before, p)

    def test_cas_bloquants_structurels(self):
        for journal, reason in [
            (entries(["2026-10-20", "2026-09-01"]) + "### 2026-08-01 — titre\n" + entries(["2026-07-01"]), "titre ###"),
            (entries(["2026-10-20", "2026-09-01"]) + "Paragraphe libre.\n" + entries(["2026-07-01", "2026-06-01"]),
             "paragraphe intercalé")]:
            with self.subTest(reason=reason):
                before = fiche(journal=journal + PAD * 6 + "\n")
                p = self.sheet(before)
                h = tree_hash(self.vault)
                code, r = self.rotate(p)
                self.assertTrue(any(reason in b for b in r["blocked"]), r)
                self.assertEqual(h, tree_hash(self.vault))

    def test_sections_protegees_jamais_deplacees(self):
        lourd = "\n".join(f"- **2025-0{1 + k % 9}-01 — Décision {k}.** {PAD}" for k in range(20))
        before = fiche(journal=entries(["2026-10-20", "2026-09-01", "2026-08-01"]),
                       after="\n## Points de vigilance\n\n" + lourd + "\n")
        p = self.sheet(before)
        code, r = self.rotate(p)
        self.assertTrue(any("reste au-dessus du budget" in b for b in r["blocked"]))
        self.assertIn(lourd, read(p))
        self.assertNoLoss(before, p)

    def test_bloc_de_code_opaque(self):
        code_block = "  ````md\n  - 2026-01-01 pas une entrée\n  ```\n  ## pas un titre\n  ````\n"
        journal = entries(["2026-10-20", "2026-10-01"]) + "- **2026-06-01 : avec code.** " + PAD + "\n" + code_block + entries(
            ["2026-05-01"])
        before = fiche(journal=journal)
        p = self.sheet(before)
        self.rotate(p)
        j = "".join(read(x) for x in self.journals(p))
        self.assertIn("- **2026-06-01 : avec code.** " + PAD + "\n" + code_block, j)
        self.assertNoLoss(before, p)

    def test_crlf_accents_sans_retour_final(self):
        before = fiche(journal=entries(["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01", "2026-05-01"]),
                       nl="\r\n").rstrip("\r\n") + " éàç"
        p = self.sheet(before)
        self.rotate(p)
        text = read(p).replace("## Journal\r\n\r\n", "## Journal\r\n\r\n" + entries(
            ["2026-10-27", "2026-10-26", "2026-10-25"]).replace("\n", "\r\n"), 1)
        before = before + "\r\n" + entries(["2026-10-27", "2026-10-26", "2026-10-25"]).replace("\n", "\r\n")
        self.write(p, text)
        self.rotate(p)
        raw = read(p, binary=True)
        self.assertNotIn(b"\n", raw.replace(b"\r\n", b""))      # aucune fin de ligne LF isolée
        self.assertNotIn(b"\r\r", raw)
        for j in self.journals(p):
            self.assertNotIn(b"\n", read(j, binary=True).replace(b"\r\n", b""))
            self.assertNotIn(b"\r\r", read(j, binary=True))
        self.assertNoLoss(before, p)

    def test_trimestre_existant_ordre_et_idempotence(self):
        before = fiche(journal=entries(["2026-10-20", "2026-10-10", "2026-09-20", "2026-09-10", "2026-08-01"]))
        p = self.sheet(before)
        self.rotate(p)
        # nouvelles entrées en tête : la fiche redépasse, les entrées de septembre rejoignent le T3 existant
        text = read(p).replace("## Journal\n\n", "## Journal\n\n" + entries(
            ["2026-10-27", "2026-10-25", "2026-10-23"]), 1)
        self.write(p, text)
        self.rotate(p)
        t3 = read([x for x in self.journals(p) if x.endswith("T3.md")][0])
        self.assertLess(t3.index("2026-09-20"), t3.index("2026-09-10"))
        self.assertLess(t3.index("2026-09-10"), t3.index("2026-08-01"))
        h = tree_hash(self.vault)
        code, r = self.rotate(p)
        self.assertEqual(r["moves"], {})
        self.assertEqual(h, tree_hash(self.vault))

    def test_simulation_n_ecrit_rien(self):
        p = self.sheet(fiche(journal=entries(["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01"])))
        h = tree_hash(self.root)
        code, r = self.rotate(p, apply=False)
        self.assertEqual(r["mode"], "simulation")
        self.assertTrue(r["moves"])
        self.assertEqual(h, tree_hash(self.root))

    def test_rotation_non_activee(self):
        self.write(os.path.join(self.vault, "_Meta", "hooks.conf"), "JOURNAL_MAX_KB_PROJECT=4\n")
        p = self.sheet(fiche(journal=entries(["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01"])))
        h = tree_hash(self.vault)
        code, r = self.rotate(p)
        self.assertEqual(code, 1)
        self.assertIn("JOURNAL_ROTATION", r["error"])
        self.assertEqual(h, tree_hash(self.vault))


class Surete(Base):
    def _plan(self, p):
        note = vj.Note(p)
        return note, vj.plan(note, vj.settings(self.vault))

    def test_ecriture_concurrente(self):
        before = fiche(journal=entries(["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01"]))
        p = self.sheet(before)
        note, plan = self._plan(p)
        def concurrent():
            with open(p, "a", encoding="utf-8") as fh:
                fh.write("ajout concurrent\n")
        vj._before_write, old = concurrent, vj._before_write
        try:
            with self.assertRaises(RuntimeError):
                vj.apply(note, plan, self.vault)
        finally:
            vj._before_write = old
        self.assertEqual(self.journals(p), [])
        self.assertEqual(read(p), before + "ajout concurrent\n")

    def test_relecture_incomplete_restaure(self):
        before = fiche(journal=entries(["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01"]))
        p = self.sheet(before)
        note, plan = self._plan(p)
        real = vj.atomic_write
        def truncating(path, text, mode=None, guard=None):
            real(path, text[: len(text) // 2] if "/journal/" in path else text, mode, guard)
        vj.atomic_write = truncating
        try:
            with self.assertRaises(RuntimeError):
                vj.apply(note, plan, self.vault)
        finally:
            vj.atomic_write = real
        self.assertEqual(read(p), before)
        self.assertEqual(self.journals(p), [])

    def test_vault_git_commit_des_seuls_chemins_touches(self):
        g = lambda *a: subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *a], cwd=self.vault,
                                      env=self.env, capture_output=True, text=True, check=True).stdout
        before = fiche(journal=entries(["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01"]))
        p = self.sheet(before)
        autre = os.path.join(self.vault, "20-Areas", "x", "x.md")
        self.write(autre, "---\ntype: area\n---\n")
        g("init", "-q"); g("add", "-A"); g("commit", "-q", "-m", "init")
        self.write(autre, "---\ntype: area\n---\nmodif en cours\n")
        self.write(p, before + "\nretouche non commitée\n")
        self.env.update(GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
        code, r = self.rotate(p)
        self.assertEqual(code, 0, r)
        self.assertEqual(r["warnings"], [])
        log = g("log", "--format=%s")
        self.assertIn("rotation du journal : alpha", log)
        self.assertIn("avant rotation du journal : alpha", log)
        status = g("status", "--porcelain")
        self.assertIn("20-Areas/x/x.md", status)
        self.assertNotIn("alpha", status)
        self.assertTrue(os.listdir(os.path.join(self.root, "state", "second-cerveau", "rotation")))

    def test_verify(self):
        a = os.path.join(self.root, "a.md"); b = os.path.join(self.root, "b.md"); c = os.path.join(self.root, "c.md")
        self.write(a, "## Suivi\n- un\n- deuxième point validé\n- trois\n")
        self.write(b, "## Journal\n- un\n")
        self.write(c, "- deuxième point validé\n- trois\n")
        self.assertEqual(self.run_cli("verify", "--before", a, "--after", b, c)[0], 1)   # titre renommé, strict
        self.assertEqual(self.run_cli("verify", "--loose", "--before", a, "--after", b, c)[0], 0)
        self.write(c, "- deuxième point validé\n")
        code, out = self.run_cli("verify", "--loose", "--before", a, "--after", b, c)
        self.assertEqual(code, 1)
        self.assertIn("- trois", json.loads(out)["missing"])
        self.write(c, "- **2026-01-01** deuxième point validé\n- trois\n")
        self.assertEqual(self.run_cli("verify", "--loose", "--before", a, "--after", b, c)[0], 0)
        # pertes réelles que --loose ne doit pas laisser passer
        self.write(a, "### 2026-03-01 — Réunion avec Louis : budget validé à 40 k€\n#client-acme\n- non\n")
        self.write(b, "- point A\n- Louis a dit non au devis\n")
        code, out = self.run_cli("verify", "--loose", "--before", a, "--after", b)
        self.assertEqual(code, 1)
        self.assertEqual(len(json.loads(out)["missing"]), 3)


class Signalement(Base):
    def test_check_et_vault_health(self):
        self.sheet(fiche(journal=entries(["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01"])))
        self.sheet(fiche(title="beta") + PAD * 50, slug="beta")
        code, out = self.run_cli("check", "--vault", self.vault)
        r = json.loads(out)
        self.assertEqual({x["path"] for x in r["over"]}, {"10-Projects/alpha/alpha.md", "10-Projects/beta/beta.md"})
        beta = [x for x in r["over"] if "beta" in x["path"]][0]
        self.assertTrue(beta["blocked"])
        payload = json.dumps({"cwd": self.vault})
        h = tree_hash(self.vault)
        out = subprocess.run(["bash", HEALTH], input=payload, env=self.env, capture_output=True, text=True).stdout
        self.assertIn("2 fiche(s) au-dessus de leur budget", json.loads(out)["hookSpecificOutput"]["additionalContext"])
        self.assertEqual(h, tree_hash(self.vault))

    def test_journaux_et_types_sans_budget_ignores(self):
        self.write(os.path.join(self.vault, "10-Projects", "alpha", "journal", "alpha-2026-T3.md"),
                   "---\ntype: journal\n---\n" + PAD * 100)
        self.write(os.path.join(self.vault, "30-Resources", "doc.md"), "---\ntype: resource\n---\n" + PAD * 100)
        self.assertEqual(json.loads(self.run_cli("check", "--vault", self.vault)[1])["over"], [])


class Revue(Base):
    """Cas issus de la revue de code de la 4.1.0."""

    def test_cloture_quatre_accents_garde_les_sections_protegees(self):
        code = "  ````md\n  ```\n  exemple\n  ```\n  ````\n"
        journal = entries(["2026-10-20", "2026-10-01"]) + "- **2026-03-01 : exemple de code.** " + PAD + "\n" + code
        before = fiche(journal=journal, after="\n## Points de vigilance\n\n- Ne jamais X.\n")
        p = self.sheet(before)
        code_, r = self.rotate(p)
        self.assertEqual(code_, 0, r)
        text = read(p)
        self.assertIn("## Décisions", text)
        self.assertIn("- Ne jamais X.", text)
        self.assertNotIn("Ne jamais X", "".join(read(j) for j in self.journals(p)))
        self.assertNoLoss(before, p)

    def test_bloc_de_code_non_ferme_ou_titre_dedans_bloque_la_fiche(self):
        for extra, reason in [("  ```\n  jamais fermé\n", "jamais refermé"),
                              ("  ```\n## Faux titre\n  ```\n", "déborde de son entrée")]:
            with self.subTest(reason=reason):
                journal = entries(["2026-10-20", "2026-10-01"]) + "- **2026-03-01 : x.** " + PAD + "\n" + extra
                p = self.sheet(fiche(journal=journal + entries(["2026-02-01", "2026-01-01"])))
                h = tree_hash(self.vault)
                code, r = self.rotate(p)
                self.assertTrue(any(reason in b for b in r["blocked"]), r)
                self.assertEqual(r["moves"], {})
                self.assertEqual(h, tree_hash(self.vault))

    def test_bloc_de_code_en_colonne_0_entre_deux_puces_bloque(self):
        journal = entries(["2026-10-20", "2026-10-01"]) + "```\ncode\n```\n" + entries(["2026-03-01", "2026-02-01"])
        p = self.sheet(fiche(journal=journal))
        code, r = self.rotate(p)
        self.assertTrue(any("bloc de code en colonne 0" in b for b in r["blocked"]), r)
        self.assertEqual(self.journals(p), [])

    def test_titre_h3_suivi_de_puces_datees_bloque(self):
        journal = "### 2026-10-20 — Réunion\n\n" + PAD + "\n\n### 2026-10-01 — Réunion\n\n" + PAD + "\n\n" + entries(
            ["2026-03-01", "2026-02-01", "2025-12-01"])
        p = self.sheet(fiche(journal=journal))
        code, r = self.rotate(p)
        self.assertTrue(any("puce datée sous un titre ###" in b for b in r["blocked"]), r)
        self.assertEqual(self.journals(p), [])

    def test_ecriture_concurrente_pendant_l_ecriture_des_journaux(self):
        before = fiche(journal=entries(["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01"]))
        p = self.sheet(before)
        note = vj.Note(p)
        plan = vj.plan(note, vj.settings(self.vault))
        real = vj.atomic_write
        done = []
        def racing(path, text, mode=None, guard=None):
            real(path, text, mode, guard)
            if "/journal/" in path and not done:
                done.append(path)
                with open(p, "a", encoding="utf-8") as fh:
                    fh.write("ajout concurrent\n")
        vj.atomic_write = racing
        try:
            with self.assertRaises(RuntimeError):
                vj.apply(note, plan, self.vault)
        finally:
            vj.atomic_write = real
        self.assertEqual(read(p), before + "ajout concurrent\n")
        self.assertEqual(self.journals(p), [])

    def test_annulation_sans_commit_git(self):
        g = lambda *a: subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *a], cwd=self.vault,
                                      env=self.env, capture_output=True, text=True, check=True).stdout
        before = fiche(journal=entries(["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01"]))
        p = self.sheet(before)
        g("init", "-q"); g("add", "-A"); g("commit", "-q", "-m", "init")
        self.write(p, before + "retouche non commitée\n")
        note = vj.Note(p)
        plan = vj.plan(note, vj.settings(self.vault))
        def concurrent():
            with open(p, "a", encoding="utf-8") as fh:
                fh.write("ajout concurrent\n")
        vj._before_write, old = concurrent, vj._before_write
        try:
            with self.assertRaises(RuntimeError):
                vj.apply(note, plan, self.vault)
        finally:
            vj._before_write = old
        self.assertEqual(g("log", "--format=%s").split(), ["init"])

    def test_sensibilite_et_cadenas_herites(self):
        text = fiche(title="alpha 🔒", journal=entries(["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01"]))
        text = text.replace("status: active\n", "status: active\nsensibilité: confidentiel\nconfidentiel: true\n")
        p = self.sheet(text)
        self.rotate(p)
        j = read(self.journals(p)[0])
        self.assertIn("sensibilité: confidentiel", j)
        self.assertIn("confidentiel: true", j)
        self.assertIn("# Journal alpha : 2026-T", j)
        self.assertIn("🔒", j.split("# Journal")[1].splitlines()[0])

    def test_index_existant_avec_alias_et_texte_libre(self):
        before = fiche(journal=entries(["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01"]),
                       after="\n## Journaux\n\nIndex des trimestres.\n- [[alpha-2025-T4|T4 2025]]\n")
        p = self.sheet(before)
        code, r = self.rotate(p)
        self.assertEqual(code, 0, r)
        text = read(p)
        self.assertIn("Index des trimestres.\n", text)
        self.assertIn("- [[alpha-2025-T4|T4 2025]]\n", text)
        self.assertIn("- [[alpha-2026-T3]]", text)
        self.assertTrue(text.endswith("\n"))
        self.assertEqual(text.count("## Journaux"), 1)
        self.assertNoLoss(before, p)

    def test_rotate_all(self):
        self.sheet(fiche(journal=entries(["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01"])))
        self.sheet(fiche(title="beta", journal=entries(["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01"])), "beta")
        code, out = self.run_cli("rotate", "--apply", "--all", "--vault", self.vault)
        self.assertEqual(code, 0, out)
        self.assertEqual({d["path"] for d in json.loads(out)}, {"10-Projects/alpha/alpha.md", "10-Projects/beta/beta.md"})
        self.assertTrue(all(d["mode"] == "écrit" for d in json.loads(out)))

    def test_deux_sections_vers_le_meme_trimestre(self):
        self.write(os.path.join(self.vault, "_Meta", "hooks.conf"), self.conf + "JOURNAL_SECTIONS=Journal,Réunions\n")
        before = fiche(journal=entries(["2026-10-20", "2026-10-01", "2026-08-01"]),
                       after="\n## Réunions\n\n" + entries(["2026-10-21", "2026-10-02", "2026-07-15"]))
        p = self.sheet(before)
        self.rotate(p)
        t3 = read([x for x in self.journals(p) if x.endswith("T3.md")][0])
        self.assertIn("2026-08-01", t3)
        self.assertIn("2026-07-15", t3)
        self.assertNoLoss(before, p)

    def test_keep_zero_et_reglage_invalide(self):
        self.write(os.path.join(self.vault, "_Meta", "hooks.conf"), "JOURNAL_KEEP=abc\nJOURNAL_MAX_KB=x\n")
        s = vj.settings(self.vault)
        self.assertEqual((s["keep"], s["default_kb"]), (5, 30))
        self.write(os.path.join(self.vault, "_Meta", "hooks.conf"), "JOURNAL_ROTATION=1\nJOURNAL_MAX_KB_PROJECT=1\nJOURNAL_KEEP=0\n")
        before = fiche(journal=entries(["2026-10-20", "2026-10-01"]))
        p = self.sheet(before)
        code, r = self.rotate(p)
        self.assertEqual(sum(r["moves"].values()), 2)
        self.assertNoLoss(before, p)

    def test_fiche_non_utf8_n_arrete_pas_le_traitement(self):
        bad = os.path.join(self.vault, "10-Projects", "bad", "bad.md")
        self.write(bad, b"---\ntype: project\n---\n\xff\xfe" + b"x" * 5000, binary=True)
        p = self.sheet(fiche(journal=entries(["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01"])))
        code, out = self.run_cli("rotate", "--apply", bad, p)
        res = json.loads(out)
        self.assertEqual(code, 1)
        self.assertIn("illisible", res[0]["error"])
        self.assertEqual(res[1]["mode"], "écrit")

    def test_sans_frontmatter_et_avec_bom(self):
        self.write(os.path.join(self.vault, "_Meta", "hooks.conf"), self.conf + "JOURNAL_MAX_KB=4\n")
        before = "\ufeff" + fiche(journal=entries(["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01"]))
        p = self.sheet(before)
        self.assertEqual(vj.Note(p).fm.get("type"), "project")
        self.rotate(p)
        self.assertNoLoss(before, p)
        sans = fiche(journal=entries(["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01"])).split("---\n", 2)[2]
        q = self.sheet(sans, "gamma")
        code, r = self.rotate(q)
        self.assertEqual(r["budget_kb"], 4)
        self.assertTrue(r["moves"])
        self.assertNoLoss(sans, q)

    def test_droits_conserves(self):
        p = self.sheet(fiche(journal=entries(["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01"])))
        os.chmod(p, 0o640)
        self.rotate(p)
        self.assertEqual(os.stat(p).st_mode & 0o777, 0o640)
        um = os.umask(0); os.umask(um)
        for j in self.journals(p):
            self.assertEqual(os.stat(j).st_mode & 0o777, 0o666 & ~um)

    def test_crlf_derniere_ligne_sans_retour_deplacee(self):
        text = ("---\ntype: project\n---\n\n# alpha\n\n## Journal\n\n" + entries(
            ["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01"])).rstrip("\n").replace("\n", "\r\n")
        p = self.sheet(text)
        self.rotate(p)
        for f in [p] + self.journals(p):
            raw = read(f, binary=True)
            self.assertNotIn(b"\n", raw.replace(b"\r\n", b""), f)
            self.assertNotIn(b"\r\r", raw, f)
        self.assertNoLoss(text, p)

    def test_lien_relatif_signale(self):
        journal = entries(["2026-10-20", "2026-10-01"]) + "- **2026-06-01 : CR.** [CR](meetings/x.md) " + PAD + "\n" + entries(
            ["2026-05-01"])
        p = self.sheet(fiche(journal=journal))
        code, r = self.rotate(p, apply=False)
        self.assertTrue(any("meetings/x.md" in w for w in r["warnings"]), r)

    def test_ecriture_concurrente_pendant_le_fsync_de_la_fiche(self):
        before = fiche(journal=entries(["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01"]))
        p = self.sheet(before)
        note = vj.Note(p)
        plan = vj.plan(note, vj.settings(self.vault))
        real = vj.os.fsync
        done = []
        def slow_fsync(fd):
            real(fd)
            try:
                name = os.readlink(f"/proc/self/fd/{fd}")
            except OSError:
                return
            if os.path.basename(name).startswith(".rotation-") and "/journal/" not in name and not done:
                done.append(name)
                with open(p, "a", encoding="utf-8") as fh:
                    fh.write("ajout pendant le fsync\n")
        vj.os.fsync = slow_fsync
        try:
            with self.assertRaises(RuntimeError):
                vj.apply(note, plan, self.vault)
        finally:
            vj.os.fsync = real
        self.assertTrue(done)
        self.assertEqual(read(p), before + "ajout pendant le fsync\n")
        self.assertEqual(self.journals(p), [])
        self.assertEqual([f for f in os.listdir(os.path.dirname(p)) if f.startswith(".rotation-")], [])

    def test_bloc_de_code_qui_deborde_de_son_entree(self):
        journal = entries(["2026-10-20"]) + "```\n" + entries(["2026-07-01"]) + "- **2026-04-01 : x.** " + PAD + "\n  ```\n" + entries(
            ["2026-01-10"])
        before = fiche(journal=journal)
        p = self.sheet(before)
        h = tree_hash(self.vault)
        code, r = self.rotate(p)
        self.assertTrue(any("déborde de son entrée" in b or "colonne 0" in b for b in r["blocked"]), r)
        self.assertEqual(h, tree_hash(self.vault))
        journal = "- **2026-01-10 : ouverture.** " + PAD + "\n  ```\n  code\n" + entries(["2026-04-01", "2026-07-01"]) + \
                  "- **2026-10-20 : bilan.** " + PAD + "\n```\n"
        self.write(os.path.join(self.vault, "_Meta", "hooks.conf"), self.conf.replace("JOURNAL_KEEP=2", "JOURNAL_KEEP=1"))
        p = self.sheet(fiche(journal=journal), "beta")
        h = tree_hash(self.vault)
        code, r = self.rotate(p)
        self.assertTrue(any("déborde de son entrée" in b for b in r["blocked"]), r)
        self.assertEqual(h, tree_hash(self.vault))

    def test_verify_loose_titre_informatif(self):
        a = os.path.join(self.root, "a.md"); b = os.path.join(self.root, "b.md")
        self.write(a, "## Suivi\n### Décision : abandon de Stripe\n### Louis quitte le projet\n- point conservé ici\n")
        self.write(b, "## Journal\n- point conservé ici\n")
        code, out = self.run_cli("verify", "--loose", "--before", a, "--after", b)
        self.assertEqual(code, 1)
        self.assertEqual(len(json.loads(out)["missing"]), 2)

    def test_index_vide_en_fin_de_fichier(self):
        for nl, final in [("\n", True), ("\r\n", True), ("\r\n", False)]:
            with self.subTest(nl=repr(nl), final=final):
                text = fiche(journal=entries(["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01"]),
                             after="\n## Journaux\n", nl=nl)
                if not final:
                    text = text.rstrip("\r\n")
                p = self.sheet(text, f"x{len(nl)}{int(final)}")
                code, r = self.rotate(p)
                self.assertEqual(code, 0, r)
                raw = read(p, binary=True)
                self.assertTrue(raw.endswith(nl.encode()), raw[-40:])
                if nl == "\r\n":
                    self.assertNotIn(b"\n", raw.replace(b"\r\n", b""))
                self.assertNoLoss(text, p)

    def test_journal_existant_non_utf8(self):
        p = self.sheet(fiche(journal=entries(["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01"])))
        self.write(os.path.join(os.path.dirname(p), "journal", "alpha-2026-T2.md"), b"\xff\xfe bad", binary=True)
        before = read(p)
        code, out = self.run_cli("rotate", "--apply", p)
        res = json.loads(out)
        self.assertEqual(code, 1)
        self.assertIn("error", res[0])
        self.assertEqual(read(p), before)

    def test_commentaire_dans_un_bloc_de_code_ne_bloque_pas(self):
        before = fiche(journal=entries(["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01"]),
                       before="## Mise en route\n\n```bash\n# installer les dépendances\n## encore un commentaire\nnpm i\n```\n\n")
        p = self.sheet(before)
        code, r = self.rotate(p)
        self.assertEqual(code, 0, r)
        self.assertTrue(r["moves"])
        self.assertIn("# installer les dépendances", read(p))
        self.assertNoLoss(before, p)

    def test_fiche_lf_avec_une_ligne_crlf(self):
        before = fiche(journal=entries(["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01"])).replace(
            "État courant.\n", "État courant.\r\n")
        p = self.sheet(before)
        self.rotate(p)
        for j in self.journals(p):
            self.assertNotIn(b"\r", read(j, binary=True))
        self.assertNoLoss(before, p)

    def test_cle_sensibilite_en_nfd(self):
        import unicodedata
        key = unicodedata.normalize("NFD", "sensibilité")
        text = fiche(journal=entries(["2026-10-20", "2026-10-01", "2026-07-01", "2026-06-01"])).replace(
            "status: active\n", f"status: active\n{key}: confidentiel\n")
        p = self.sheet(text)
        self.rotate(p)
        self.assertIn("confidentiel", read(self.journals(p)[0]))

    def test_date_isolee_epinglee(self):
        journal = entries(["2026-10-20", "2026-10-10", "2016-10-05", "2026-09-01", "2026-08-01", "2026-07-01"])
        before = fiche(journal=journal)
        p = self.sheet(before)
        code, r = self.rotate(p)
        self.assertIn("2016-10-05", read(p))
        self.assertFalse(any("2016" in k for k in r["moves"]))
        self.assertNoLoss(before, p)


if __name__ == "__main__":
    unittest.main(verbosity=2)
