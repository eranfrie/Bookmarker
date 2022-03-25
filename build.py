import pathlib

import pycodestyle

from src.utils import paths


def main():
    exit_code = 0

    project_root_dir = paths.get_project_root_dir()
    pep8_config_file = pathlib.Path(project_root_dir, "pep8.conf")
    result = pycodestyle.StyleGuide(config_file=pep8_config_file) \
        .check_files([project_root_dir])
    if result.total_errors > 0:
        exit_code = 1

    exit(exit_code)


if __name__ == "__main__":
    main()
