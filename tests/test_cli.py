import unittest
from unittest.mock import patch

from src.infrastructure.cli import PasswordManagerCLI


class PasswordManagerCliTests(unittest.TestCase):
    @patch("builtins.input", side_effect=["register", "alice", "correcthorsebatterystaple", "exit"])
    def test_interactive_register_flow(self, _mock_input: object) -> None:
        cli = PasswordManagerCLI()
        result = cli.dispatch([])
        self.assertEqual(result, "Au revoir.")

    def test_register_add_and_list_via_cli(self) -> None:
        cli = PasswordManagerCLI()

        register_result = cli.dispatch(["register", "alice", "correcthorsebatterystaple"])
        self.assertIn("registered", register_result.lower())

        add_result = cli.dispatch([
            "add",
            "GitHub",
            "alice",
            "Secr3t123",
            "correcthorsebatterystaple",
        ])
        self.assertIn("added", add_result.lower())

        items = cli.dispatch(["list", "correcthorsebatterystaple"])
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["service"], "GitHub")
        self.assertEqual(items[0]["password"], "Secr3t123")
