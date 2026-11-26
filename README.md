# GhostWriter-Plugins

[English](README.en.md) · Deutsch

Optionale Erweiterungen für [GhostWriter](https://github.com/ploeffler/GhostWriter). Jedes Plugin liegt in einem eigenen Ordner `plugins/<name>/` und hat eigene Versionen (Tag je Plugin, z. B. `film-v0.3.0`). Bücher bekommen eingeschaltete Plugins über den täglichen Update-Lauf.

Das Format (`plugin.yml`, Anleitungen je Chat-Programm) wird in [#2](https://github.com/ploeffler/ghostwriter-plugins/issues/2) festgelegt. Geplant: [Film](https://github.com/ploeffler/ghostwriter-plugins/issues/3), [Guide](https://github.com/ploeffler/ghostwriter-plugins/issues/1).

## Prüfen

Wie im Hauptrepo: lokal nur die Tests des geänderten Plugins, die übrigen Prüfungen macht `validate` auf GitHub.

```
python scripts/run_tests.py --plugin film     # Tests eines Plugins
python scripts/run_tests.py --shared          # Tests der gemeinsamen Skripte
python scripts/run_tests.py                   # alles, parallel je Modul
git diff --name-only origin/main > /tmp/changed.txt && python scripts/select_tests.py --files /tmp/changed.txt
```

`validate` lässt im Pull Request nur die Tests der geänderten Plugins laufen. Gemeinsame Skripte, Workflows und `requirements.txt` lösen die volle Suite aus, reine Textänderungen gar keine Tests. Auf `main` laufen die Tests nicht noch einmal, wenn der Pull Request denselben Stand schon vollständig und grün geprüft hat.

Commit-Nachrichten und Doku auf Deutsch.
