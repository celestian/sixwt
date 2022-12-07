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
def step_impl(context):

    try:
        os.remove(context.scenario_config_file)
    except OSError:
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred

    assert context.scenario_config_file.is_file() is False


@given("sixwt is properly configured")
def step_impl(context):
    assert context.scenario_config_file.is_file() is True


@given("storage directory is missing")
def step_impl(context):
    cfg = read_configuration(context.scenario_config_file)
    storage = abs_path(cfg["sixwt"]["storage_folder"])
    assert storage.is_dir() is False


@given("storage directory exists")
def step_impl(context):
    command = "sixwt init"
    completed_process = subprocess.run(
        command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    assert completed_process.returncode == 0
    context.config.stdout_capture = None
    context.config.stderr_capture = None


@given("storage directory exists with catalog examples")
def step_impl(context):
    command = "sixwt init --with-examples"
    completed_process = subprocess.run(
        command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    assert completed_process.returncode == 0
    context.config.stdout_capture = None
    context.config.stderr_capture = None


@when('we run "{command}" non-interactively')
def step_impl(context, command):
    completed_process = subprocess.run(
        command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    context.return_code = completed_process.returncode
    context.stdout = completed_process.stdout.decode("utf-8")
    context.stderr = completed_process.stderr.decode("utf-8")


@when('we run "{command}" with "{answers}"')
def step_impl(context, command):

    if context.cli_options:
        command = command + " " + context.cli_options

    # TODO nacti answers, zadavej odpovedi do promptu

    proc = subprocess.Popen(
        command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
    )
    try:
        outs, errs = proc.communicate(timeout=15)
    except TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()

    # TODO remove


#    print("[return_code] >>>", context.return_code)
#    print("[completed_process.stdout] >>>", completed_process.stdout.decode("utf-8"))
#    print(
#        "[completed_process.stderr] >>>",
#        completed_process.stderr.decode("utf-8"),
#        file=sys.stderr,
#    )
#


@then('return code is "{return_code}"')
def step_impl(context, return_code):
    assert context.return_code == int(return_code)


@then('we see "{text}" on stdout')
def step_impl(context, text):
    if context.stdout:
        print(">>>> out", context.stdout)
        assert text in context.stdout


@then('we see "{text}" on stderr')
def step_impl(context, text):
    if context.stderr:
        print(">>>> err", context.stderr)
        assert text in context.stderr


@then('file "{file_name}" is created')
def step_impl(context, file_name):  # noqa: F811
    assert Path(file_name).is_file()


@then("storage directory exists")
def step_impl(context):
    cfg = read_configuration(context.scenario_config_file)
    storage = abs_path(cfg["sixwt"]["storage_folder"])
    characters = storage.joinpath("characters")
    catalog = storage.joinpath("catalog")
    assert storage.is_dir() is True
    assert characters.is_dir() is True
    assert catalog.is_dir() is True


@then("catalog examples are created")
def step_impl(context):
    cfg = read_configuration(context.scenario_config_file)
    storage = abs_path(cfg["sixwt"]["storage_folder"])
    catalog = storage.joinpath("catalog")
    example_file = catalog.joinpath("priority_table", "metatype.csv")
    assert example_file.is_file() is True


@then("db file exists")
def step_impl(context):
    cfg = read_configuration(context.scenario_config_file)
    storage = abs_path(cfg["sixwt"]["storage_folder"])
    db_file = storage.joinpath("sixwt.db")
    assert db_file.is_file() is True
