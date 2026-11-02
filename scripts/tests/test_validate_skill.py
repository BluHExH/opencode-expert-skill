import importlib.util
import json
import pathlib
import tempfile
import unittest

SCRIPT_PATH = pathlib.Path(__file__).resolve().parents[2] / "scripts" / "validate_skill.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_skill_under_test", str(SCRIPT_PATH))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestValidateSkill(unittest.TestCase):
    def setUp(self):
        self.validator = load_validator()

    def _make_skill(self, tmp, frontmatter_body, readme="ok\n", manifest='[{"topic": "t", "source_type": "official documentation", "source_url": "https://example.com", "verification_status": "DOCUMENTED"}]\n'):
        root = pathlib.Path(tmp) / "sample-skill"
        root.mkdir(parents=True, exist_ok=True)
        (root / "SKILL.md").write_text("---\n" + frontmatter_body + "\n---\n\n# Sample\n", encoding="utf-8")
        (root / "README.md").write_text(readme, encoding="utf-8")
        (root / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")
        src = root / "sources"
        src.mkdir(parents=True, exist_ok=True)
        (src / "official-documentation.md").write_text("# Docs\n", encoding="utf-8")
        (src / "source-code-map.md").write_text("# Map\n", encoding="utf-8")
        (src / "source-manifest.json").write_text(manifest, encoding="utf-8")
        (src / "version-history.md").write_text("# History\n", encoding="utf-8")
        refs = root / "references"
        refs.mkdir(parents=True, exist_ok=True)
        (refs / "01-opencode-overview.md").write_text("# Overview\n", encoding="utf-8")
        return root

    def test_valid_skill_has_no_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_skill(tmp, "name: sample-skill\ndescription: A sample skill for testing.")
            findings = self.validator.run_checks(root)
            errors = [f for f in findings if f.severity == "ERROR"]
            self.assertEqual(errors, [])

    def test_missing_description_is_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_skill(tmp, "name: sample-skill\n")
            findings = self.validator.run_checks(root)
            errors = [f for f in findings if f.severity == "ERROR"]
            self.assertTrue(any("description" in f.message.lower() for f in errors))

    def test_invalid_name_is_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_skill(tmp, "name: Bad_Name\ndescription: A sample skill for testing.")
            findings = self.validator.run_checks(root)
            errors = [f for f in findings if f.severity == "ERROR"]
            self.assertTrue(any("Invalid skill name" in f.message for f in errors))

    def test_broken_link_is_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_skill(tmp, "name: sample-skill\ndescription: A sample skill for testing.")
            (root / "SKILL.md").write_text(
                "---\nname: sample-skill\ndescription: A sample skill for testing.\n---\n\n# Sample\n\nSee [missing](references/does-not-exist.md).\n",
                encoding="utf-8",
            )
            findings = self.validator.run_checks(root)
            errors = [f for f in findings if f.severity == "ERROR"]
            self.assertTrue(any("Broken markdown link target" in f.message for f in errors))

    def test_invalid_source_manifest_json_is_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_skill(tmp, "name: sample-skill\ndescription: A sample skill for testing.", manifest="{not valid json")
            findings = self.validator.run_checks(root)
            errors = [f for f in findings if f.severity == "ERROR"]
            self.assertTrue(any("not valid JSON" in f.message for f in errors))

    def test_empty_required_file_is_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_skill(tmp, "name: sample-skill\ndescription: A sample skill for testing.", readme="")
            findings = self.validator.run_checks(root)
            errors = [f for f in findings if f.severity == "ERROR"]
            self.assertTrue(any("Required file is empty" in f.message for f in errors))

    def test_unbalanced_mermaid_fence_is_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_skill(tmp, "name: sample-skill\ndescription: A sample skill for testing.")
            (root / "SKILL.md").write_text(
                "---\nname: sample-skill\ndescription: A sample skill for testing.\n---\n\n# Sample\n\n```mermaid\nflowchart TD\n A --> B\n",
                encoding="utf-8",
            )
            findings = self.validator.run_checks(root)
            errors = [f for f in findings if f.severity == "ERROR"]
            self.assertTrue(any("Unbalanced code fence" in f.message for f in errors))

    def test_mermaid_without_keyword_is_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_skill(tmp, "name: sample-skill\ndescription: A sample skill for testing.")
            (root / "SKILL.md").write_text(
                "---\nname: sample-skill\ndescription: A sample skill for testing.\n---\n\n# Sample\n\n```mermaid\nthis is not a diagram\n```\n",
                encoding="utf-8",
            )
            findings = self.validator.run_checks(root)
            warnings = [f for f in findings if f.severity == "WARNING"]
            self.assertTrue(any("Mermaid block without recognized diagram keyword" in f.message for f in warnings))


if __name__ == "__main__":
    unittest.main()