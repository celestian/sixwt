# Copyright (C) 2022 sixwt Contributors, see LICENSE

import os
import shutil
import tempfile
from pathlib import Path


def before_all(context):
    """Setup environemnt before all behaves"""

    context.main_test_dir = tempfile.mkdtemp(prefix="sixwt_behave-")

    context.base_wd = os.getcwd()
    context.base_config_file = Path(context.base_wd).joinpath(
        "features", "data", "sixwt.conf"
    )


def after_all(context):
    """Clean up environment after all behaves"""

    debug = os.getenv("SIXWT_BEHAVE_DEBUG")
    if debug and "1" == debug:
        print(f"DEBUG: Behave test dir is [{context.main_test_dir}]")
    else:
        shutil.rmtree(context.main_test_dir)
        context.main_test_dir = None


def before_feature(context, feature):
    """Setup before each feature"""
    context.feature_test_dir = Path(context.main_test_dir).joinpath(
        feature.name.replace(" ", "_")
    )
    if not context.feature_test_dir.is_dir():
        os.makedirs(context.feature_test_dir)


def before_scenario(context, scenario):
    """Setup environment before each scenario"""
    context.scenario_test_dir = context.feature_test_dir.joinpath(
        scenario.name.replace(" ", "_")
    )

    if not context.scenario_test_dir.is_dir():
        os.makedirs(context.scenario_test_dir)

    context.scenario_config_file = context.scenario_test_dir.joinpath("sixwt.conf")
    shutil.copyfile(context.base_config_file, context.scenario_config_file)

    os.chdir(context.scenario_test_dir)
