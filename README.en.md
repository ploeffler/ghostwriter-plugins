# GhostWriter plugins

English · [Deutsch](README.md)

Optional extensions for [GhostWriter](https://github.com/ploeffler/GhostWriter). Each plugin lives in its own folder `plugins/<name>/` and has its own versions (one tag per plugin, e.g. `film-v0.3.0`). Books receive enabled plugins through the daily update run.

The format (`plugin.yml`, instructions per chat client) is being defined in [#2](https://github.com/ploeffler/ghostwriter-plugins/issues/2). Planned: [Film](https://github.com/ploeffler/ghostwriter-plugins/issues/3), [Guide](https://github.com/ploeffler/ghostwriter-plugins/issues/1).

## Checks

As in the main repository: locally run only the tests of the plugin you changed; `validate` on GitHub does the rest.

```
python scripts/run_tests.py --plugin film     # one plugin's tests
python scripts/run_tests.py --shared          # tests of the shared scripts
python scripts/run_tests.py                   # everything, in parallel per module
git diff --name-only origin/main > /tmp/changed.txt && python scripts/select_tests.py --files /tmp/changed.txt
```

In a pull request, `validate` runs only the tests of the changed plugins. Shared scripts, workflows and `requirements.txt` trigger the full suite; text-only changes run no tests. On `main`, tests are not repeated when the pull request already checked the same tree fully and successfully.
