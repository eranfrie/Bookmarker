from pathlib import Path
import sys

import pycodestyle
import pylint.lint
import pytest

from src.utils import paths


def main():
    exit_code = 0
    project_root_dir = paths.get_project_root_dir()

    # pycodestyle
    print("Running pycodestyle ...")
    pep8_config_file = Path(project_root_dir, "pep8.conf")
    result = pycodestyle.StyleGuide(config_file=pep8_config_file) \
        .check_files([project_root_dir])
    if result.total_errors == 0:
        print("SUCCEEDED\n")
    else:
        print("FAILED\n")
        exit_code = 1
    print("=" * 80, "\n")

    # pylint
    print("Running pylint ...")
    rc_file = str(Path(project_root_dir, ".pylintrc"))
    src_dir = str(Path(project_root_dir, "src"))
    # pylint doesn't return anything - just prints to screen
    pylint.lint.Run(["--rcfile=" + rc_file, src_dir], exit=False)

    # pytest
    res = pytest.main()
    if res != pytest.ExitCode.OK:
        exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
