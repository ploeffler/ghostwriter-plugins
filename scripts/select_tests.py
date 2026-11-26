#!/usr/bin/env python3
"""Testumfang aus den geänderten Dateien bestimmen (wie im Hauptrepo, #439/#485).

Jedes Plugin liegt in `plugins/<name>/` und hat seine Tests in `plugins/<name>/tests/`.
Ändert ein Pull Request nur Dateien in einzelnen Plugins, laufen nur deren Tests.
Alles andere (gemeinsame Skripte, Workflows, `tests/`, Abhängigkeiten, gelöschte
Dateien außerhalb eines Plugins) führt zur vollen Suite. Reine Text-Dateien
(README, LICENSE, *.md außerhalb von Plugins) brauchen keine Tests.

  python scripts/select_tests.py --files /tmp/changed.txt [--removed /tmp/removed.txt]
  python scripts/select_tests.py --files /tmp/changed.txt --github-output "$GITHUB_OUTPUT"

Ausgabe: mode=full|subset|none und plugins=<namen, durch Leerzeichen getrennt>.
"""
import argparse
import re
import sys
from pathlib import Path

PLUGIN = re.compile(r'^plugins/([a-z0-9][a-z0-9-]*)/')
NO_TESTS = re.compile(r'^(README(\.[a-z]{2})?\.md|LICENSE|\.gitignore|docs/.*\.md)$')


def select(changed, removed=()):
    """Gibt (mode, plugins) zurück."""
    plugins = set()
    for path in removed:
        if not PLUGIN.match(path) and not NO_TESTS.match(path):
            return 'full', []
    for path in [*changed, *removed]:
        m = PLUGIN.match(path)
        if m:
            plugins.add(m.group(1))
        elif NO_TESTS.match(path):
            continue
        else:
            return 'full', []
    if not plugins:
        return 'none', []
    return 'subset', sorted(plugins)


def read(path):
    if not path:
        return []
    return [line.strip() for line in Path(path).read_text(encoding='utf-8').splitlines() if line.strip()]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--files', required=True, help='Datei mit den geänderten Pfaden, einer je Zeile')
    ap.add_argument('--removed', help='Datei mit gelöschten bzw. umbenannten Pfaden')
    ap.add_argument('--github-output', help='Ergebnis zusätzlich an diese Datei anhängen')
    a = ap.parse_args(argv)
    mode, plugins = select(read(a.files), read(a.removed))
    out = f'mode={mode}\nplugins={" ".join(plugins)}\n'
    print(out, end='')
    if a.github_output:
        with open(a.github_output, 'a', encoding='utf-8') as fh:
            fh.write(out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
