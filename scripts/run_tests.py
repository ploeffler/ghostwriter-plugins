#!/usr/bin/env python3
"""Testmodule parallel ausführen und ihre Laufzeit melden (wie im Hauptrepo, #485).

Gesammelt werden `tests/test_*.py` (gemeinsame Skripte) und `plugins/<name>/tests/test_*.py`.
Jedes Modul läuft in einem eigenen Prozess, so viele gleichzeitig wie Kerne da sind,
größere Module zuerst. Am Schluss stehen die langsamsten Module.

  python scripts/run_tests.py                    # alles
  python scripts/run_tests.py --plugin film      # nur die Tests dieses Plugins (mehrfach möglich)
  python scripts/run_tests.py --shared           # nur tests/
  python scripts/run_tests.py --jobs 1           # nacheinander

Ergebnis: 0, wenn alle Module grün sind (auch wenn es noch keine Tests gibt); sonst 1.
"""
import argparse
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def collect(plugins=None, shared=False):
    """Liste der Testdateien. plugins=None und shared=False: alles."""
    files = []
    if shared or plugins is None:
        files += sorted((ROOT / 'tests').glob('test_*.py'))
    if plugins is None:
        files += sorted(ROOT.glob('plugins/*/tests/test_*.py'))
    else:
        for name in plugins:
            files += sorted((ROOT / 'plugins' / name / 'tests').glob('test_*.py'))
    return sorted(files, key=lambda f: (-f.stat().st_size, str(f)))


def run_module(path):
    env = dict(os.environ, PYTHONPATH=os.pathsep.join(filter(None, [
        str(path.parent), str(path.parent.parent), str(ROOT / 'scripts'), os.environ.get('PYTHONPATH')])))
    start = time.monotonic()
    r = subprocess.run([sys.executable, '-m', 'unittest', path.stem], cwd=path.parent, env=env,
                       capture_output=True, text=True)
    return path.relative_to(ROOT).as_posix(), r.returncode, time.monotonic() - start, r.stdout + r.stderr


def count(output):
    m = re.search(r'^Ran (\d+) tests?', output, re.M)
    return int(m.group(1)) if m else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--plugin', action='append', help='nur die Tests dieses Plugins')
    ap.add_argument('--shared', action='store_true', help='nur die gemeinsamen Tests unter tests/')
    ap.add_argument('--jobs', type=int, default=os.cpu_count() or 1, help='gleichzeitige Prozesse')
    ap.add_argument('--slowest', type=int, default=10)
    a = ap.parse_args(argv)
    if a.plugin:
        unknown = [p for p in a.plugin if not (ROOT / 'plugins' / p).is_dir()]
        if unknown:
            print('Unbekannte Plugins: ' + ', '.join(unknown), file=sys.stderr)
            return 1
    files = collect(a.plugin, a.shared)
    if not files:
        print('Keine Tests gefunden – nichts zu tun.')
        return 0
    start = time.monotonic()
    with ThreadPoolExecutor(max_workers=max(1, a.jobs)) as pool:
        results = list(pool.map(run_module, files))
    wall = time.monotonic() - start
    failed = [r for r in results if r[1] != 0]
    for name, _, _, output in failed:
        print(f'\n===== {name}: rot =====\n{output}')
    total = sum(count(r[3]) for r in results)
    print(f'\n{total} Tests in {len(results)} Modulen, {wall:.1f} s ({a.jobs} Prozesse)')
    print('Langsamste Module:')
    for name, code, secs, _ in sorted(results, key=lambda r: -r[2])[:a.slowest]:
        print(f'  {secs:6.1f} s  {name}' + ('  (rot)' if code else ''))
    if failed:
        print(f'\n{len(failed)} Modul(e) rot: ' + ', '.join(r[0] for r in failed))
        return 1
    print('OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
