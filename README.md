# SixWT

[![run_tests](https://github.com/celestian/sixwt/actions/workflows/run_tests.yml/badge.svg)](https://github.com/celestian/sixwt/actions/workflows/run_tests.yml)

## About
This is a tool for Shadowrun 6th edition.

## Technical details

    # dependencies
    sudo dnf install nox sqlite

    # dependencies (for development)
    sudo dnf install python3-devel graphviz graphviz-devel

    # dev environment
    nox -s dev
    source .venv/bin/activate

    # run tests with debug
    SIXWT_BEHAVE_DEBUG=1 nox -s behave

## Resources
- [conventional commits](https://www.conventionalcommits.org)
- [setuptools](https://setuptools.pypa.io/en/latest/userguide/index.html)
- [nox](https://nox.thea.codes/en/stable/)
- [behave](https://behave.readthedocs.io)
- [docopt](http://docopt.org/)
- [inquirerpy](https://inquirerpy.readthedocs.io/en/latest/index.html)
- [transitions](https://github.com/pytransitions/transitions#quickstart)
