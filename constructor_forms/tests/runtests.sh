#!/bin/sh
export PYTHONPATH="./"

django-admin.py test --settings=constructor_forms.tests.settings $@
