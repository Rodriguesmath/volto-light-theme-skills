"""Tests for check_vlt_conventions.py and repository integrity."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CHECKER = REPO_ROOT / "skills" / "volto-light-theme" / "scripts" / "check_vlt_conventions.py"


class TestCheckVltConventions(unittest.TestCase):
    def _run_checker(self, target: Path, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), str(target), *extra],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_clean_addon_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src"
            (src / "theme").mkdir(parents=True)
            (src / "theme" / "_root.scss").write_text(":root { --theme-color: #ffffff; }\n")
            (src / "theme" / "main.scss").write_text(".hero { color: var(--theme-color); display: flex; }\n")
            (src / "App.tsx").write_text("export const App = () => <div className='hero' />;\n")

            res = self._run_checker(src, "--strict")
            self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_evals_score_response_ignores_comments_and_catches_real_code(self) -> None:
        sys.path.insert(0, str(REPO_ROOT / "evals"))
        import run_evals

        case = {
            "id": "t",
            "must_contain": ["var(--theme-", "rem"],
            "must_not_contain": ["position: absolute", "#26364a"],
        }
        good = "```scss\n// stripped position: absolute and #26364a\n.box { padding: 1rem; color: var(--theme-foreground-color); }\n```"
        bad = "```scss\n.box { position: absolute; padding: 1rem; color: var(--theme-foreground-color); }\n```"
        self.assertEqual(run_evals.score_response(case, good), (True, []))
        ok, failures = run_evals.score_response(case, bad)
        self.assertFalse(ok)
        self.assertIn("forbidden found: 'position: absolute'", failures)

    def test_detects_semantic_ui_import_and_ui_selector_as_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src"
            src.mkdir(parents=True)
            (src / "Bad.tsx").write_text("import { Button } from 'semantic-ui-react';\n")
            (src / "bad.scss").write_text(".wrapper .ui.menu { color: var(--theme-color); }\n")

            res = self._run_checker(src, "--format", "json")
            self.assertEqual(res.returncode, 1)
            data = json.loads(res.stdout)
            self.assertEqual(data["errors"], 2)
            rules = {i["rule"] for i in data["issues"]}
            self.assertEqual(rules, {"no-semantic-ui-react", "no-ui-selector"})

    def test_detects_warnings_and_fails_only_in_strict_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src"
            (src / "customizations").mkdir(parents=True)
            (src / "customizations" / "Logo.tsx").write_text("export default () => null;\n")
            (src / "card.scss").write_text(".card { position: absolute; color: #123456; }\n")

            res_normal = self._run_checker(src, "--format", "json")
            self.assertEqual(res_normal.returncode, 0)
            data = json.loads(res_normal.stdout)
            self.assertEqual(data["errors"], 0)
            self.assertEqual(data["warnings"], 3)

            res_strict = self._run_checker(src, "--strict")
            self.assertEqual(res_strict.returncode, 1)

            res_err_only = self._run_checker(src, "--errors-only", "--format", "json")
            self.assertEqual(res_err_only.returncode, 0)
            err_data = json.loads(res_err_only.stdout)
            self.assertEqual(err_data["warnings"], 0)
            self.assertEqual(err_data["issues"], [])

    def test_evals_validate_only(self) -> None:
        runner = REPO_ROOT / "evals" / "run_evals.py"
        res = subprocess.run(
            [sys.executable, str(runner), "--validate-only"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_evals_score_response_ignores_comments_and_catches_real_code(self) -> None:
        sys.path.insert(0, str(REPO_ROOT / "evals"))
        import run_evals

        case = {
            "id": "t",
            "must_contain": ["var(--theme-", "rem"],
            "must_not_contain": ["position: absolute", "#26364a"],
        }
        good = "```scss\n// stripped position: absolute and #26364a\n.box { padding: 1rem; color: var(--theme-foreground-color); }\n```"
        bad = "```scss\n.box { position: absolute; padding: 1rem; color: var(--theme-foreground-color); }\n```"
        self.assertEqual(run_evals.score_response(case, good), (True, []))
        ok, failures = run_evals.score_response(case, bad)
        self.assertFalse(ok)
        self.assertIn("forbidden found: 'position: absolute'", failures)

    def test_all_skills_have_valid_frontmatter(self) -> None:
        skills_dir = REPO_ROOT / "skills"
        for skill_md in skills_dir.glob("*/SKILL.md"):
            content = skill_md.read_text(encoding="utf-8")
            self.assertTrue(content.startswith("---\n"), f"Missing frontmatter in {skill_md}")
            self.assertIn("name:", content[:400])
            self.assertIn("description:", content[:600])


if __name__ == "__main__":
    unittest.main()
