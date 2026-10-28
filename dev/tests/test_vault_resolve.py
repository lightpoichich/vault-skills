#!/usr/bin/env python3
"""Tests de hooks/vault-resolve.py et du hook Stop hooks/vault-sync-nudge.sh.

  python3 dev/tests/test_vault_resolve.py

Chaque test monte un HOME temporaire (vault, dépôts git, dossiers sans git) et lance les scripts en
sous-processus : `vault-resolve.py` lit HOME à l'import. Dépendances : python3, git, bash.
"""
import json, os, subprocess, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RESOLVE = os.path.join(ROOT, "hooks", "vault-resolve.py")
NUDGE = os.path.join(ROOT, "hooks", "vault-sync-nudge.sh")
GIT_ID = ["-c", "user.name=t", "-c", "user.email=t@t", "-c", "init.defaultBranch=main"]


def write(path, text=""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def sheet(vault, slug, **fields):
    lines = ["---", "type: project", "status: active"]
    for k, v in fields.items():
        k = k.replace("_", "-")
        if isinstance(v, list) and v and v[0] == "BLOCK":
            lines.append(f"{k}:")
            lines += [f"  - {x}" for x in v[1:]]
        elif isinstance(v, list):
            lines.append(f"{k}: [{', '.join(v)}]")
        else:
            lines.append(f"{k}: {v}")
    lines += ["---", f"# {slug}", ""]
    write(os.path.join(vault, "10-Projects", slug, f"{slug}.md"), "\n".join(lines))


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = os.path.realpath(self.tmp.name)
        self.vault = os.path.join(self.home, "vault-reel")
        os.makedirs(os.path.join(self.vault, "_Meta"))
        os.makedirs(os.path.join(self.vault, "_personas", "chief-of-staff"))
        write(os.path.join(self.vault, "_Meta", "hooks.conf"), "SYNC_MIN_KB=0\nSYNC_MIN_MINUTES=0\n")
        os.symlink(self.vault, os.path.join(self.home, "vault"))
        self.env = {k: v for k, v in os.environ.items() if k != "CLAUDE_PROJECT_DIR"}
        self.env.update(HOME=self.home, XDG_CACHE_HOME=os.path.join(self.home, ".cache"),
                        GIT_CONFIG_NOSYSTEM="1")

    def tearDown(self):
        self.tmp.cleanup()

    def mkdir(self, *parts):
        d = os.path.join(self.home, *parts)
        os.makedirs(d, exist_ok=True)
        return d

    def git(self, cwd, *args):
        subprocess.run(["git", *GIT_ID, *args], cwd=cwd, env=self.env, check=True, capture_output=True)

    def repo(self, *parts, remote=None):
        d = self.mkdir(*parts)
        self.git(d, "init", "-q")
        self.git(d, "commit", "-q", "--allow-empty", "-m", "init")
        if remote:
            self.git(d, "remote", "add", "origin", remote)
        return d

    def resolve(self, d):
        r = subprocess.run([sys.executable, RESOLVE, d], env=self.env, capture_output=True, text=True, check=True)
        return json.loads(r.stdout)

    def nudge(self, d):
        transcript = os.path.join(self.home, "transcript.jsonl")
        write(transcript, "x" * 2048)
        payload = json.dumps({"session_id": "s-" + os.path.basename(d), "transcript_path": transcript, "cwd": d})
        r = subprocess.run(["bash", NUDGE], input=payload, env=self.env, capture_output=True, text=True)
        return json.loads(r.stdout) if r.stdout.strip() else None

    def assertProjet(self, d, slug, match):
        r = self.resolve(d)
        self.assertEqual((r["mode"], os.path.basename(r["sheet"]), r["match"]), ("projet", f"{slug}.md", match))
        return r


class Resolve(Base):
    def test_vault_et_persona(self):
        self.assertEqual(self.resolve(self.vault)["mode"], "vault")
        self.assertEqual(self.resolve(os.path.join(self.vault, "_personas", "chief-of-staff"))["mode"], "vault")

    def test_depot_relie_par_repo(self):
        sheet(self.vault, "alpha", repo="git@github.com:org/Alpha.git")
        d = self.repo("code", "alpha-local", remote="https://github.com/org/alpha")
        r = self.assertProjet(d, "alpha", "repo")
        self.assertEqual(r["repo"], "https://github.com/org/alpha")

    def test_depot_relie_par_repo_sous_dossier(self):
        sheet(self.vault, "api", repo="https://github.com/org/mono#apps/api")
        sheet(self.vault, "mono", repo="https://github.com/org/mono")
        d = self.repo("code", "mono", remote="https://github.com/org/mono.git")
        self.assertProjet(os.path.join(self.mkdir("code", "mono", "apps", "api", "src")), "api", "repo")
        self.assertProjet(d, "mono", "repo")

    def test_depot_relie_par_dossier_travail(self):
        d = self.repo("code", "beta-local")
        sheet(self.vault, "beta", dossier_travail=d)
        self.assertProjet(d, "beta", "dossier-travail")

    def test_depot_relie_par_slug(self):
        sheet(self.vault, "gamma")
        d = self.repo("code", "gamma")
        self.assertProjet(self.mkdir("code", "gamma", "src"), "gamma", "slug")
        self.assertProjet(d, "gamma", "slug")

    def test_sans_git_dossier_travail_scalaire_et_sous_dossier(self):
        d = self.mkdir("OneDrive", "Client Delta")
        sheet(self.vault, "delta", dossier_travail=f'"{d}"')
        r = self.assertProjet(d, "delta", "dossier-travail")
        self.assertEqual((r["repo"], r["subpath"]), ("", ""))
        self.assertProjet(self.mkdir("OneDrive", "Client Delta", "Compta", "2026"), "delta", "dossier-travail")

    def test_sans_git_liste_en_ligne_et_en_bloc(self):
        d1 = self.mkdir("OneDrive", "epsilon")
        d2 = self.mkdir("OneDrive", "zeta")
        sheet(self.vault, "epsilon", dossier_travail=["/Users/x/OneDrive/epsilon", d1])
        sheet(self.vault, "zeta", dossier_travail=["BLOCK", "/mnt/c/Users/x/OneDrive/zeta", d2])
        self.assertProjet(d1, "epsilon", "dossier-travail")
        self.assertProjet(d2, "zeta", "dossier-travail")

    def test_sans_git_le_plus_specifique_gagne(self):
        large = self.mkdir("OneDrive", "Clients")
        precis = self.mkdir("OneDrive", "Clients", "eta")
        sheet(self.vault, "clients", dossier_travail=large)
        sheet(self.vault, "eta", dossier_travail=precis)
        self.assertProjet(os.path.join(precis), "eta", "dossier-travail")
        self.assertProjet(self.mkdir("OneDrive", "Clients", "autre"), "clients", "dossier-travail")

    def test_sans_git_pas_de_repli_par_slug(self):
        sheet(self.vault, "theta")
        self.assertEqual(self.resolve(self.mkdir("Documents", "theta"))["mode"], "none")

    def test_dossier_travail_home_ignore(self):
        sheet(self.vault, "iota", dossier_travail=self.home)
        sheet(self.vault, "kappa", dossier_travail="/")
        self.assertEqual(self.resolve(self.mkdir("Documents", "divers"))["mode"], "none")

    def test_gabarit_ignore(self):
        sheet(self.vault, "lambda", dossier_travail="{ chemin absolu | absent }")
        self.assertEqual(self.resolve(self.mkdir("Documents", "lambda-x"))["mode"], "none")

    def test_sans_lien(self):
        sheet(self.vault, "mu", repo="https://github.com/org/mu")
        self.assertEqual(self.resolve(self.mkdir("Documents", "rien"))["mode"], "none")
        self.assertEqual(self.resolve(self.repo("code", "rien-git", remote="https://github.com/org/x"))["mode"], "none")


class Nudge(Base):
    def test_vault(self):
        out = self.nudge(self.vault)
        self.assertEqual(out["decision"], "block")
        self.assertIn("sync-vault", out["reason"])
        self.assertNotIn("mode projet", out["reason"])

    def test_depot_relie(self):
        sheet(self.vault, "alpha", repo="https://github.com/org/alpha")
        out = self.nudge(self.repo("code", "alpha", remote="https://github.com/org/alpha"))
        self.assertIn("sync-vault (mode projet)", out["reason"])
        self.assertIn("dans le dépôt https://github.com/org/alpha", out["reason"])
        self.assertIn("commits récents", out["reason"])

    def test_dossier_sans_git_relie(self):
        d = self.mkdir("OneDrive", "delta")
        sheet(self.vault, "delta", dossier_travail=d)
        out = self.nudge(d)
        self.assertIn("sync-vault (mode projet)", out["reason"])
        self.assertIn(f"dans le dossier {d}", out["reason"])
        self.assertNotIn("commits", out["reason"])
        self.assertNotIn("sync-repo", out["reason"])

    def test_sans_lien_silencieux(self):
        self.assertIsNone(self.nudge(self.mkdir("Documents", "rien")))

    def test_worktree_silencieux(self):
        sheet(self.vault, "alpha", repo="https://github.com/org/alpha")
        main = self.repo("code", "alpha", remote="https://github.com/org/alpha")
        wt = os.path.join(self.home, "worktrees", "alpha-ticket")
        self.git(main, "worktree", "add", "-q", wt)
        self.assertEqual(self.resolve(wt)["mode"], "projet")
        self.assertIsNone(self.nudge(wt))

    def test_sync_nudge_vault_coupe_les_dossiers(self):
        write(os.path.join(self.vault, "_Meta", "hooks.conf"), "SYNC_MIN_KB=0\nSYNC_MIN_MINUTES=0\nSYNC_NUDGE=vault\n")
        d = self.mkdir("OneDrive", "delta")
        sheet(self.vault, "delta", dossier_travail=d)
        self.assertIsNone(self.nudge(d))
        self.assertIsNotNone(self.nudge(self.vault))


def line(kind, **kw):
    """Une ligne de transcript Claude Code : ("filler", n), ("skill", nom), ("slash", nom), ("edit", chemin)."""
    ts = {"timestamp": "2020-01-01T00:00:00.000Z"}
    if kind == "filler":
        return json.dumps({"type": "user", "message": {"content": "x" * kw["n"]}, **ts})
    if kind == "slash":
        return json.dumps({"type": "user", "message": {"content": f"<command-name>/{kw['name']}</command-name>"}, **ts})
    tool = {"skill": ("Skill", {"skill": kw.get("name", "")}), "edit": ("Edit", {"file_path": kw.get("path", "")})}[kind]
    return json.dumps({"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": tool[0], "input": tool[1]}]}, **ts})


class NudgeSyncFaitSansRappel(Base):
    """Une répercussion faite sans le rappel pose une nouvelle base : pas de rappel pour ce qui vient d'être fait."""

    def setUp(self):
        super().setUp()
        write(os.path.join(self.vault, "_Meta", "hooks.conf"), "SYNC_MIN_KB=2\nSYNC_MIN_MINUTES=0\n")

    def run_nudge(self, d, lines):
        transcript = os.path.join(self.home, "t.jsonl")
        write(transcript, "\n".join(lines) + "\n")
        payload = json.dumps({"session_id": "s-" + self.id(), "transcript_path": transcript, "cwd": d})
        r = subprocess.run(["bash", NUDGE], input=payload, env=self.env, capture_output=True, text=True)
        return json.loads(r.stdout) if r.stdout.strip() else None

    def test_sans_sync_rappel(self):
        out = self.run_nudge(self.vault, [line("filler", n=4000)])
        self.assertIn("Rien à répercuter.", out["reason"])

    def test_skill_sync_a_la_main_silence(self):
        self.assertIsNone(self.run_nudge(self.vault, [
            line("filler", n=4000), line("skill", name="second-cerveau:sync-vault"), line("filler", n=200)]))

    def test_commande_slash_silence(self):
        self.assertIsNone(self.run_nudge(self.vault, [
            line("filler", n=4000), line("slash", name="second-cerveau:sync-vault"), line("filler", n=200)]))

    def test_travail_apres_sync_rappel(self):
        out = self.run_nudge(self.vault, [
            line("filler", n=4000), line("skill", name="second-cerveau:sync-vault"), line("filler", n=4000)])
        self.assertIsNotNone(out)

    def test_autre_skill_rappel(self):
        out = self.run_nudge(self.vault, [line("filler", n=4000), line("skill", name="second-cerveau:audit-vault")])
        self.assertIsNotNone(out)

    def test_mode_projet_fiche_ecrite_silence(self):
        d = self.mkdir("OneDrive", "delta")
        sheet(self.vault, "delta", dossier_travail=d)
        via_lien = os.path.join(self.home, "vault", "10-Projects", "delta", "delta.md")
        self.assertIsNone(self.run_nudge(d, [line("filler", n=4000), line("edit", path=via_lien)]))

    def test_mode_projet_autre_fichier_rappel(self):
        d = self.mkdir("OneDrive", "delta")
        sheet(self.vault, "delta", dossier_travail=d)
        out = self.run_nudge(d, [line("filler", n=4000), line("edit", path=os.path.join(d, "notes.md"))])
        self.assertIn("mode projet", out["reason"])

    def test_mode_vault_fiche_ecrite_rappel(self):
        # Depuis le vault, écrire une fiche n'est pas une sync : les décisions touchent souvent d'autres fiches.
        sheet(self.vault, "delta")
        path = os.path.join(self.vault, "10-Projects", "delta", "delta.md")
        self.assertIsNotNone(self.run_nudge(self.vault, [line("filler", n=4000), line("edit", path=path)]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
