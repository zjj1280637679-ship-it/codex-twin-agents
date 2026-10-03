import json
import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "open-task-twin"
    / "scripts"
    / "twin_fork.py"
)


def run_cli(*args: str):
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    return proc, json.loads(proc.stdout) if proc.stdout.strip() else None


class TwinForkCliTests(unittest.TestCase):
    def test_open_defaults_to_full_history(self):
        proc, payload = run_cli(
            "open",
            "--fork-id",
            "test-open",
            "--task-name",
            "open-twin",
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(payload["spawn_agent"]["fork_turns"], "all")
        self.assertTrue(payload["same_context"])
        self.assertFalse(
            payload["fork_handle"]["inheritance"]["local_strategy"]
        )
        self.assertFalse(
            payload["fork_handle"]["inheritance"]["local_metrics"]
        )

    def test_directed_requires_objective(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "directed"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("requires --objective", proc.stderr)

    def test_bounded_fork_is_accepted_and_warned(self):
        proc, payload = run_cli(
            "verify",
            "--fork-turns",
            "3",
            "--fork-id",
            "test-bounded",
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(payload["spawn_agent"]["fork_turns"], "3")
        self.assertTrue(payload["warnings"])

    def test_none_is_not_claimed_as_same_context(self):
        proc, payload = run_cli(
            "open",
            "--fork-turns",
            "none",
            "--fork-id",
            "test-none",
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertFalse(payload["same_context"])
        self.assertIn("clean-context child", payload["warnings"][0])

    def test_spawn_args_only_matches_codex_shape(self):
        proc, payload = run_cli(
            "open",
            "--fork-id",
            "test-shape",
            "--spawn-args-only",
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(
            set(payload),
            {"task_name", "message", "fork_turns"},
        )
        self.assertEqual(payload["fork_turns"], "all")


if __name__ == "__main__":
    unittest.main()
