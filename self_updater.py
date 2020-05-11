import git
from pathlib import Path

repo = git.Repo(Path('.').absolute())
origin = repo.remotes.origin
origin.pull()
