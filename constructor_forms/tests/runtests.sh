#!/bin/sh
export PYTHONPATH="./"

django-admin.py test --settings=settings $@