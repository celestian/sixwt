#!/usr/bin/env bash

if [ "$1" == "" ]
then

    echo "./clean.sh (cache|envs)"

elif [ "$1" == "cache" ]
then

    find . | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf

elif [ "$1" == "envs" ]
then

    if [ -z ${VIRTUAL_ENV+x} ]
    then

        find . | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf
        rm -rf build
        rm -rf sixwt.egg-info
        rm -rf .venv
        rm -rf .nox

    else

        echo "Please, deactivate virtual env first."

    fi
fi
