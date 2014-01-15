#!/bin/sh

django-admin.py test --settings=constructor_forms.tests.settings $@
