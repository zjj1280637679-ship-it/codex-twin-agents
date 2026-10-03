import json
import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills" / "open-task-twin" / "scripts" / "twin_fork.py"
)


def run_cli(*args: str):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        text=True, encoding="utf-8", capture_output=True, check=False,
    )


class TwinForkCliTests(unittest.TestCase):
    def test_no_arguments_produce_direct_native_request(self):
        proc = run_cli()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(set(payload), {"task_name", "message", "fork_turns"})
        self.assertRegex(payload["task_name"], r"^[a-z0-9_]+$")
        self.assertEqual(payload["fork_turns"], "all")
        self.assertTrue(payload["message"].strip())

    def test_user_message_is_preserved_without_added_instructions(self):
        message = '检查刚才的修改。\n保留 "用户验收条件"，不要重写。'
        proc = run_cli("--task-name", "verification_twin", "--message", message)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["task_name"], "verification_twin")
        self.assertEqual(payload["message"], message)

    def test_native_context_options_are_passed_through(self):
        for turns in ("all", "none", "1", "3"):
            with self.subTest(turns=turns):
                proc = run_cli("--fork-turns", turns, "--message", "Inspect available evidence.")
                self.assertEqual(proc.returncode, 0, proc.stderr)
                payload = json.loads(proc.stdout)
                self.assertEqual(payload["fork_turns"], turns)
                self.assertEqual(payload["message"], "Inspect available evidence.")

    def test_rejects_invalid_native_context_arguments(self):
        for turns in ("0", "-1", "many"):
            with self.subTest(turns=turns):
                proc = run_cli("--fork-turns", turns)
                self.assertEqual(proc.returncode, 2)
                self.assertFalse(proc.stdout)

    def test_rejects_task_names_outside_native_schema(self):
        for name in ("context-twin", "Twin", "two twins", ""):
            with self.subTest(name=name):
                proc = run_cli("--task-name", name)
                self.assertEqual(proc.returncode, 2)
                self.assertFalse(proc.stdout)


if __name__ == "__main__":
    unittest.main()
