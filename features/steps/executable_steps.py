# Copyright (C) 2022 sixwt Contributors, see LICENSE

import errno
import os
import shutil
import subprocess
from pathlib import Path

from behave import given, then, when  # pylint: disable=no-name-in-module
from steps.utils import abs_path, read_configuration

# pylint: disable=function-redefined


@given("we have sixwt installed")
def step_impl(context):  # noqa: F811
    assert shutil.which("sixwt") is not None


@given("sixwt is not properly configured")
def step_impl(context):  # noqa: F811

    try:
        os.remove(context.scenario_config_file)
    except OSError as error:
        if error.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred

    assert context.scenario_config_file.is_file() is False


@given("sixwt is properly configured")
def step_impl(context):  # noqa: F811
    assert context.scenario_config_file.is_file() is True


@given("storage directory is missing")
def step_impl(context):  # noqa: F811
    cfg = read_configuration(context.scenario_config_file)
    storage = abs_path(cfg["sixwt"]["storage_folder"])
    assert storage.is_dir() is False


@given("storage directory exists")
def step_impl(context):  # noqa: F811
    command = "sixwt init"
    completed_process = subprocess.run(
        command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    assert completed_process.returncode == 0


@given("storage directory exists with catalog examples")
def step_impl(context):  # noqa: F811
    command = "sixwt init --with-examples"
    completed_process = subprocess.run(
        command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    assert completed_process.returncode == 0


@when('we run "{command}" non-interactively')
def step_impl(context, command):  # noqa: F811
    completed_process = subprocess.run(
        command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    context.return_code = completed_process.returncode
    context.stdout = completed_process.stdout.decode("utf-8")
    context.stderr = completed_process.stderr.decode("utf-8")


@when('we run "{command}" with "{answers}"')
def step_impl(context, command):  # noqa: F811
    raise NotImplementedError('WHEN: we run "{command}" with "{answers}"')


@then('return code is "{return_code}"')
def step_impl(context, return_code):  # noqa: F811
    assert context.return_code == int(return_code)


@then('we see "{text}" on stdout')
def step_impl(context, text):  # noqa: F811
    if context.stdout:
        assert text in context.stdout


@then('we see "{text}" on stderr')
def step_impl(context, text):  # noqa: F811
    if context.stderr:
        assert text in context.stderr


@then('file "{file_name}" is created')
def step_impl(context, file_name):  # noqa: F811
    assert Path(file_name).is_file()


@then("storage directory exists")
def step_impl(context):  # noqa: F811
    cfg = read_configuration(context.scenario_config_file)
    storage = abs_path(cfg["sixwt"]["storage_folder"])
    characters = storage.joinpath("characters")
    catalog = storage.joinpath("catalog")
    assert storage.is_dir() is True
    assert characters.is_dir() is True
    assert catalog.is_dir() is True


@then("catalog examples are created")
def step_impl(context):  # noqa: F811
    cfg = read_configuration(context.scenario_config_file)
    storage = abs_path(cfg["sixwt"]["storage_folder"])
    catalog = storage.joinpath("catalog")
    example_file = catalog.joinpath("priority_table", "metatype.csv")
    assert example_file.is_file() is True


@then("db file exists")
def step_impl(context):  # noqa: F811
    cfg = read_configuration(context.scenario_config_file)
    storage = abs_path(cfg["sixwt"]["storage_folder"])
    db_file = storage.joinpath("sixwt.db")
    assert db_file.is_file() is True
