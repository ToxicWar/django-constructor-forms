# coding: utf-8
from __future__ import unicode_literals
from django.forms import fields


class SomeField(fields.CharField):
    '''
    Some field for test extra fields
    '''


class MyIntegerField(fields.IntegerField):
    '''
    Integer field for test extra fields
    '''
