import os
from pathlib import Path

import nox

# It's a good idea to keep your dev session out of the default list
# so it's not run twice accidentally
nox.options.sessions = [
    "black-3.10",
    "pylint-3.10",
    "flake8-3.10",
    "isort-3.10",
    "behave-3.10",
]  # Sessions other than 'dev'


# this VENV_DIR constant specifies the name of the dir that the `dev`
# session will create, containing the virtualenv;
# the `resolve()` makes it portable
VENV_DIR = Path("./.venv").resolve()

nox.options.reuse_existing_virtualenvs = True


@nox.session
def dev(session: nox.Session) -> None:
    """
    Sets up a python development environment for the project.

    This session will:
    - Create a python virtualenv for the session
    - Install the `virtualenv` cli tool into this environment
    - Use `virtualenv` to create a global project virtual environment
    - Invoke the python interpreter from the global project environment to install
      the project and all it's development dependencies.
    """

    session.install("virtualenv")
    # the VENV_DIR constant is explained above
    session.run("virtualenv", os.fsdecode(VENV_DIR), silent=True)

    python = os.fsdecode(VENV_DIR.joinpath("bin/python"))

    # Use the venv's interpreter to install the project along with
    # all it's dev dependencies, this ensures it's installed in the right way
    session.run(python, "-m", "pip", "install", "-e", ".[dev]", external=True)

    print("\n--------------------------------------------")
    print('Activate your "development" environemt with:')
    if os.name == "posix":
        print("    source .venv/bin/activate")
    else:
        print(r"    .venv\Scripts\activate")
    print("--------------------------------------------\n")


@nox.session(python=["3.10"])
def black(session):
    """Nox run black"""
    session.install("black")
    session.run("black", "--check", ".")


@nox.session(python=["3.10"])
def pylint(session: nox.Session) -> None:
    """Runs pylint checks on python files"""
    session.install(".")
    session.install("pylint")
    session.install("behave")
    session.install("nox")

    session.run("pylint", "./sixwt")
    session.run("pylint", "./features")
    session.run("pylint", "noxfile.py")


@nox.session(python=["3.10"])
def flake8(session: nox.Session) -> None:
    """Runs flake8 checks on python files"""
    session.install(".")
    session.install("flake8")

    session.run("flake8", "--max-line-length=88", "./sixwt")
    session.run("flake8", "--max-line-length=88", "./features")
    session.run("flake8", "--max-line-length=88", "noxfile.py")


@nox.session(python=["3.10"])
def isort(session: nox.Session) -> None:
    """Run check import sorting using isort"""
    session.install(".")
    session.install("isort")

    session.run("isort", "--check", "./sixwt")
    session.run("isort", "--check", "./features")
    session.run("isort", "--check", "noxfile.py")


@nox.session(python=["3.10"])
def behave(session: nox.Session) -> None:
    """Run behave tests"""
    session.install(".")
    session.install("behave")

    debug = int(os.getenv("SIXWT_BEHAVE_DEBUG", 0))
    if debug:
        session.run(
            "behave",
            "-v",
            "--no-capture",
            "--no-capture-stderr",
            "features/",
        )
    else:
        session.run("behave", "features/")
