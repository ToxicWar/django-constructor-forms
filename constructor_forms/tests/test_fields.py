# coding: utf-8
from __future__ import unicode_literals
from django.test import TestCase
from django.conf import settings
from .test_app.fields import MyIntegerField, SomeField
from .test_app.widgets import MyTextInput
from .. import fields


class FieldsTest(TestCase):
    def setUp(self):
        settings.CONSTRUCTOR_FORMS_MODIFICATION_WIDGETS[11] = 'constructor_forms.tests.test_app.widgets.MyTextInput'
        settings.CONSTRUCTOR_FORMS_EXTRA_FIELDS.append(
            (100, 'constructor_forms.tests.test_app.fields.SomeField', 'Some field')
        )
        settings.CONSTRUCTOR_FORMS_EXTRA_FIELDS.append(
            (101, 'constructor_forms.tests.test_app.fields.MyIntegerField', 'My integer field')
        )
        reload(fields)

    def tearDown(self):
        settings.CONSTRUCTOR_FORMS_MODIFICATION_WIDGETS = {}
        settings.CONSTRUCTOR_FORMS_EXTRA_FIELDS = []
        reload(fields)

    def test_widgets_conf(self):
        self.assertTrue(fields.WIDGETS[11], MyTextInput)

    def test_extra_fields_conf(self):
        self.assertTrue(fields.CLASSES[100], SomeField)
        self.assertTrue(fields.CLASSES[101], MyIntegerField)
