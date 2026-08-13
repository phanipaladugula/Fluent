History rewrite script
======================

This folder contains `reconstruct_history.py` which generates a backdated
commit plan and (optionally) applies it by creating a new branch
`reconstructed-history` filled with staged commits.

Important notes
- The script reads the current working tree's tracked files and writes a
  `.history_plan.json` at the repository root for review before applying.
- Running with `--apply` will create an orphan branch and commit files in the
  order in the plan. This is a destructive local rewrite and should be
  reviewed before pushing to any remote.
- The script does NOT push to any remote. If you decide to push, do so with
  care; forcing rewritten history onto a shared branch may disrupt collaborators.

- Script files excluded: The `scripts/` folder, the `reconstruct_history.py` script,
  and `scripts/HISTORY_REWRITE.md` (plus the generated `.history_plan.json`) are
  intentionally excluded from the generated commit plan and will not be included
  in the reconstructed commits. The script only stages and commits project files.

Quick commands

Create plan only (review before applying):

```bash
python scripts/reconstruct_history.py --plan-only
```

Apply the plan (creates branch `reconstructed-history`):

```bash
python scripts/reconstruct_history.py --apply
```

If you want to tune the number of commits, use `--commits N` and re-run.

After applying, inspect the new branch locally and push manually if desired:

```bash
git checkout reconstructed-history
git log --oneline --graph
# when satisfied
# git push origin reconstructed-history
```
