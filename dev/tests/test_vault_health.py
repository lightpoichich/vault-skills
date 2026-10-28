#!/usr/bin/env python3
"""Tests du rappel d'audit de hooks/vault-health.sh.

  python3 dev/tests/test_vault_health.py

Chaque test monte un HOME temporaire (vault, état du plugin) et lance le hook en sous-processus.
"""
import hashlib, json, os, subprocess, tempfile, time, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HEALTH = os.path.join(ROOT, "hooks", "vault-health.sh")


def write(path, text=""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


class AuditReminder(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = os.path.realpath(self.tmp.name)
        self.vault = os.path.join(self.home, "vault")
        os.makedirs(os.path.join(self.vault, "_Meta"))
        self.env = dict(os.environ, HOME=self.home, XDG_STATE_HOME=os.path.join(self.home, "state"))
        self.env.pop("CLAUDE_PROJECT_DIR", None)

    def tearDown(self):
        self.tmp.cleanup()

    def health(self):
        out = subprocess.run(["bash", HEALTH], input=json.dumps({"cwd": self.vault}), env=self.env,
                             capture_output=True, text=True).stdout
        return json.loads(out)["hookSpecificOutput"]["additionalContext"] if out.strip() else ""

    def report(self, days_ago, where="00-Inbox"):
        day = time.strftime("%Y-%m-%d", time.localtime(time.time() - days_ago * 86400))
        write(os.path.join(self.vault, where, f"audit-vault-{day}.md"), "---\ntype: audit\n---\n")

    def first_seen(self, days_ago):
        key = hashlib.sha256(os.path.realpath(self.vault).encode()).hexdigest()[:12]
        write(os.path.join(self.home, "state", "second-cerveau", "audit", key), f"{int(time.time() - days_ago * 86400)}\n")

    def test_audit_recent_silence(self):
        self.report(3)
        self.assertNotIn("audit", self.health())

    def test_audit_ancien_signale(self):
        self.report(45)
        self.assertIn("dernier audit il y a 45 j (audit-vault)", self.health())

    def test_le_plus_recent_compte_archive_comprise(self):
        self.report(90)
        self.report(5, where="40-Archive/audits")
        self.assertNotIn("audit", self.health())

    def test_sans_rapport_premiere_session_silence_puis_rappel(self):
        self.assertNotIn("audit", self.health())
        self.first_seen(31)
        self.assertIn("aucun audit depuis 31 j (audit-vault)", self.health())

    def test_reglage_zero_coupe(self):
        write(os.path.join(self.vault, "_Meta", "hooks.conf"), "AUDIT_REMINDER_DAYS=0\n")
        self.report(90)
        self.assertNotIn("audit", self.health())

    def test_reglage_delai(self):
        write(os.path.join(self.vault, "_Meta", "hooks.conf"), "AUDIT_REMINDER_DAYS=7\n")
        self.report(10)
        self.assertIn("dernier audit il y a 10 j", self.health())


if __name__ == "__main__":
    unittest.main(verbosity=2)
