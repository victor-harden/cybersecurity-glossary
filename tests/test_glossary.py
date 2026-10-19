import contextlib
import io
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import glossary


class GlossaryTests(unittest.TestCase):
    def setUp(self):
        self.terms = glossary.load()

    def test_dataset_size(self):
        self.assertGreaterEqual(len(self.terms), 60)

    def test_unique_terms(self):
        names = [t["term"] for t in self.terms]
        self.assertEqual(len(names), len(set(names)))

    def test_every_term_has_definition_and_tags(self):
        for term in self.terms:
            self.assertTrue(term["definition"].strip())
            self.assertTrue(term["tags"])

    def test_search_by_definition(self):
        results = glossary.search(self.terms, "injection")
        self.assertTrue(any("injection" in t["term"].lower() for t in results))

    def test_get_exact_term(self):
        term = glossary.get(self.terms, "cve")
        self.assertIsNotNone(term)
        self.assertEqual(term["term"], "CVE")

    def test_get_missing_term(self):
        self.assertIsNone(glossary.get(self.terms, "nonexistent-term"))

    def test_by_tag(self):
        results = glossary.by_tag(self.terms, "crypto")
        self.assertTrue(results)
        self.assertTrue(all("crypto" in t["tags"] for t in results))

    def test_cli_search_json(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = glossary.main(["--search", "tls", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(buf.getvalue())
        self.assertTrue(payload)

    def test_cli_missing_term_exit_code(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(glossary.main(["--term", "nope"]), 1)

    def test_cli_quiz(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = glossary.main(["--quiz", "3", "--seed", "42"])
        self.assertEqual(code, 0)
        self.assertIn("Answers:", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
