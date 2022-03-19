import pathlib

import git


MAJOR = 0
MINOR = 1


def get_patch():
    """Return number of commits.

    If executed from the git repo, returns number of commits.
    Otherwise, returns "<NOT-GIT-REPO>".
    """
    # path of this file (to allow running from outside of the git repo)
    git_root_dir = pathlib.Path(__file__).parent.parent.resolve()

    try:
        repo = git.Repo(git_root_dir)
        num_commits = repo.git.rev_list('--count', 'HEAD')
        return num_commits
    except git.exc.InvalidGitRepositoryError:
        return "<NOT-GIT-REPO>"


def get_version():
    return f"{MAJOR}.{MINOR}.{get_patch()}"
