import pathlib


def get_project_root_dir():
    """Return the root directory of the project.

    This is the directory of README.md.

    Returns:
        str
    """
    return str(pathlib.Path(__file__).parent.parent.parent.resolve())
