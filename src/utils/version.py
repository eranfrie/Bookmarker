import git

from utils import paths


MAJOR = 1
MINOR = 3


def get_patch():
    """Return number of commits.

    If executed from the git repo, returns number of commits.
    Otherwise, returns "<NOT-GIT-REPO>".
    """
    # use path of root dir instead of relative "."
    # (to allow running from outside of the git repo)
    git_root_dir = paths.get_project_root_dir()

    try:
        repo = git.Repo(git_root_dir)
        num_commits = repo.git.rev_list('--count', 'HEAD')
        return num_commits
    except git.InvalidGitRepositoryError:
        return "<NOT-GIT-REPO>"


def get_version():
    return f"{MAJOR}.{MINOR}.{get_patch()}"
