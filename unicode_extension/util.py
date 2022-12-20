import os
import sys


def get_project_path() -> str:
    """Get Project Path

    For path associated logic.
    It returns appropriate path of project in various situation.
    (Run by Ulauncher, Command line, VSCode Debug, Unittest)

    Returns:
        String of project path

        Example: `"."`, `"/home/{user}/.local/share/ulauncher/extensions/{extension}"`
    """
    project_path = "."

    # # Each Value per situation
    #
    # VSCode Debug (`Ulauncher Extension Debug` of this project):
    #
    # - `sys.argv`: ['main.py', '/home/{user}/.local/share/ulauncher/extensions/{extension}']
    # - `os.getcwd()`: '/home/{user}/.local/share/ulauncher/extensions/{extension}'
    #
    # Ulauncher:
    #
    # - `sys.argv`: ['/home/{user}/.local/share/ulauncher/extensions/{extension}/main.py']
    # - `os.getcwd()`: '/home/{user}'
    #
    # Python (`python unicode_extension/util.py`):
    #
    # - `sys.argv`: ['unicode_extension/util.py']
    # - `os.getcwd()`: '/home/{user}/.local/share/ulauncher/extensions/{extension}'
    #
    # Unittest (VSCode):
    #
    # - `sys.argv`: ['/home/{user}/.vscode/extensions/ms-python.python...', ..., '--testFile=/home/{extension}/.local/share/ulauncher/extensions/{extension}/{test_file_path}']
    # - `os.getcwd()`: '/home/{user}/.local/share/ulauncher/extensions/{extension}'

    if (
        (len(sys.argv) >= 2)
        and (sys.argv[0].startswith("main.py"))
        and ("ulauncher/extensions" in sys.argv[1])
    ):
        project_path = os.getcwd()
    elif (len(sys.argv) >= 1) and sys.argv[-1].startswith("--testFile"):
        project_path = os.getcwd()
    else:
        project_path = os.path.dirname(sys.argv[0])

    # if sys.argv[0].startswith("main.py") and "ulauncher" in sys.argv[1]:

    return project_path


if __name__ == "__main__":
    print(get_project_path())
