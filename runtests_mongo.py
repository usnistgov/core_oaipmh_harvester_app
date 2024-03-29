#!/usr/bin/env python
""" Run tests for MongoDB configuration
"""
import django
import os
import sys
from django.conf import settings
from django.core.management import execute_from_command_line
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.test_settings")
    execute_from_command_line(["", "migrate"])
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(interactive=False, tags=["mongodb"])
    failures = test_runner.run_tests(["tests"])
    sys.exit(bool(failures))
