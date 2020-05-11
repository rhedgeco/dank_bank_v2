import git
from pathlib import Path


class Updater:
    def on_patch(self, req, resp):
        repo = git.Repo(Path('.').absolute())
        origin = repo.remotes.origin
        origin.pull()

        for submodule in repo.submodules:
            submodule.update(init=True)
