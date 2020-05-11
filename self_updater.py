import git
from pathlib import Path

my_repo = git.Repo(Path('.').absolute())
my_repo.head.reset(index=True, working_tree=True)
fetch_info = my_repo.remotes.origin.fetch('master:master')
for info in fetch_info:
    print('{} {} {}'.format(info.ref, info.old_commit, info.flags))