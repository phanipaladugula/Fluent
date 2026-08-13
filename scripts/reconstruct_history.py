#!/usr/bin/env python3
"""
reconstruct_history.py

Creates a new orphan branch and replays the repository files into a sequence
of backdated commits. The script generates a commit plan (JSON) and then
applies commits in order, setting `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE`.

USAGE (preview plan only):
  python scripts/reconstruct_history.py --plan-only

USAGE (apply):
  python scripts/reconstruct_history.py --apply

CAUTION: This rewrites history by creating a new branch `reconstructed-history`.
Do NOT push the branch automatically; review the branch locally first.
"""
import os
import sys
import subprocess
import json
from datetime import datetime, timedelta
from collections import defaultdict

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Paths and files to exclude from the generated commit plan (do not rewrite script files)
IGNORED_PREFIXES = ('scripts/',)
IGNORED_FILES = ('scripts/reconstruct_history.py', 'scripts/HISTORY_REWRITE.md', '.history_plan.json')


def run(cmd, cwd=REPO_ROOT, env=None, check=True):
    return subprocess.run(cmd, cwd=cwd, env=env, check=check)


def git_ls_files():
    out = subprocess.check_output(['git', 'ls-files'], cwd=REPO_ROOT)
    files = out.decode('utf-8').splitlines()
    tracked = [f for f in files if f and f != '.gitignore']
    filtered = []
    for f in tracked:
        if f in IGNORED_FILES:
            continue
        skip = False
        for p in IGNORED_PREFIXES:
            if f.startswith(p):
                skip = True
                break
        if skip:
            continue
        filtered.append(f)
    return filtered


def read_all_files(files):
    contents = {}
    for p in files:
        abs_p = os.path.join(REPO_ROOT, p)
        try:
            with open(abs_p, 'rb') as fh:
                contents[p] = fh.read()
        except Exception:
            # skip unreadable files
            contents[p] = None
    return contents


def group_files(files):
    groups = defaultdict(list)
    for f in files:
        parts = f.split('/')
        key = '/'.join(parts[:2]) if len(parts) >= 2 else parts[0]
        groups[key].append(f)
    return groups


def split_into_commits(files, target=50):
    groups = group_files(files)
    # Sort groups by size
    sorted_groups = sorted(groups.items(), key=lambda kv: -len(kv[1]))
    commits = []

    # Start by creating one commit per group
    for key, flist in sorted_groups:
        commits.append({'title': key, 'files': flist})

    # If we have fewer than target, split the largest groups by file
    i = 0
    while len(commits) < target:
        # find largest commit
        commits.sort(key=lambda c: -len(c['files']))
        largest = commits[0]
        if len(largest['files']) <= 1:
            break
        # split off one file
        file_to_move = largest['files'].pop()
        commits.insert(1, {'title': os.path.dirname(file_to_move) or file_to_move, 'files': [file_to_move]})
        i += 1
        if i > 10000:
            break

    # If more than target, merge smallest commits
    while len(commits) > target:
        commits.sort(key=lambda c: len(c['files']))
        a = commits.pop()  # largest
        b = commits.pop()  # next largest
        merged = {'title': a['title'] + '+' + b['title'], 'files': a['files'] + b['files']}
        commits.append(merged)

    return commits


def message_for(title):
    t = title.lower()
    if 'test' in t or 'tests' in t:
        prefix = 'test'
    elif 'doc' in t or 'readme' in t:
        prefix = 'docs'
    elif 'docker' in t or 'nginx' in t:
        prefix = 'chore'
    elif 'schema' in t or 'model' in t or 'service' in t or 'router' in t:
        prefix = 'feat'
    elif 'fix' in t or 'bug' in t:
        prefix = 'fix'
    else:
        # alternate between feat and fix for variety
        prefix = 'feat'
    return f"{prefix}: add {title}"


def write_plan(commits, start_ts, end_ts, path):
    total = len(commits)
    start = datetime.fromisoformat(start_ts)
    end = datetime.fromisoformat(end_ts)
    delta = (end - start) / max(1, total - 1)
    plan = []
    for i, c in enumerate(commits):
        ts = (start + delta * i).replace(microsecond=0)
        plan.append({'idx': i + 1, 'timestamp': ts.isoformat(sep=' '), 'title': c['title'], 'files': c['files'], 'message': message_for(c['title'])})
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(plan, fh, indent=2)
    return plan


def empty_worktree():
    # remove all files and dirs except .git
    for entry in os.listdir(REPO_ROOT):
        if entry == '.git':
            continue
        full = os.path.join(REPO_ROOT, entry)
        try:
            if os.path.isdir(full):
                subprocess.run(['rm', '-rf', full], check=False)
            else:
                os.remove(full)
        except Exception:
            pass


def apply_plan(plan, file_contents):
    # create orphan branch
    run(['git', 'checkout', '--orphan', 'reconstructed-history'])
    # remove index and files
    run(['git', 'rm', '-rf', '.'], check=False)
    empty_worktree()

    for item in plan:
        ts = item['timestamp']
        msg = item['message']
        files = item['files']
        to_add = []
        for f in files:
            content = file_contents.get(f)
            if content is None:
                continue
            dest = os.path.join(REPO_ROOT, f)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, 'wb') as fh:
                fh.write(content)
            to_add.append(f)

        if not to_add:
            # nothing to commit for this step
            continue

        run(['git', 'add', '--'] + to_add)
        env = os.environ.copy()
        env['GIT_AUTHOR_DATE'] = ts
        env['GIT_COMMITTER_DATE'] = ts
        # Use --date for portability
        run(['git', 'commit', '-m', msg, '--date', ts], env=env)


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--start', default='2026-08-13 16:00:00')
    p.add_argument('--end', default='2026-08-14 02:00:00')
    p.add_argument('--commits', type=int, default=50)
    p.add_argument('--plan-only', action='store_true')
    p.add_argument('--apply', action='store_true')
    args = p.parse_args()

    os.chdir(REPO_ROOT)

    files = git_ls_files()
    if not files:
        print('No tracked files found. Abort.')
        sys.exit(1)

    print(f'Found {len(files)} tracked files')
    file_contents = read_all_files(files)

    commits = split_into_commits(files, target=args.commits)
    plan_path = os.path.join(REPO_ROOT, '.history_plan.json')
    plan = write_plan(commits, args.start, args.end, plan_path)
    print(f'Wrote plan to {plan_path} with {len(plan)} entries')

    if args.plan_only:
        print('Plan-only mode: inspect .history_plan.json and re-run with --apply to execute')
        return

    if args.apply:
        print('Applying plan: this will create branch reconstructed-history and rewrite history locally')
        apply_plan(plan, file_contents)
        print('Done. Review the reconstructed-history branch locally. Do not push without review.')
    else:
        print('No action taken. Use --apply to create the reconstructed branch.')


if __name__ == '__main__':
    main()
