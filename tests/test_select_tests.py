import unittest

from select_tests import select


class SelectTests(unittest.TestCase):
    def test_nur_ein_plugin(self):
        self.assertEqual(select(['plugins/film/scripts/budget.py', 'plugins/film/README.md']),
                         ('subset', ['film']))

    def test_zwei_plugins(self):
        self.assertEqual(select(['plugins/guide/plugin.yml', 'plugins/film/ANLEITUNG.md']),
                         ('subset', ['film', 'guide']))

    def test_gemeinsames_skript_voll(self):
        self.assertEqual(select(['plugins/film/x.py', 'scripts/build_wrappers.py']), ('full', []))

    def test_workflow_voll(self):
        self.assertEqual(select(['.github/workflows/validate.yml']), ('full', []))

    def test_nur_text_keine_tests(self):
        self.assertEqual(select(['README.md', 'README.en.md', 'LICENSE']), ('none', []))

    def test_geloescht_ausserhalb_voll(self):
        self.assertEqual(select(['plugins/film/a.py'], removed=['scripts/alt.py']), ('full', []))

    def test_geloescht_im_plugin(self):
        self.assertEqual(select([], removed=['plugins/guide/tests/test_alt.py']), ('subset', ['guide']))


if __name__ == '__main__':
    unittest.main()
