#!/bin/bash
SCRIPT_PATH=`dirname $0`

export DJANGO_SETTINGS_MODULE=core_oaipmh_harvester_app.settings_test
python -m unittest discover -s ${SCRIPT_PATH}/.. -p "tests_int*.py"
