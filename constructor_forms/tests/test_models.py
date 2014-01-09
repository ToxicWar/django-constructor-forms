# coding: utf-8
from __future__ import unicode_literals
from django.test import TestCase
from django.db.models import get_model
from django.utils.timezone import now
from ..conf import FORM_MODEL, FIELD_MODEL, FORM_ENTRY_MODEL, FIELD_ENTRY_MODEL


Form = get_model(*FORM_MODEL.split('.'))
Field = get_model(*FIELD_MODEL.split('.'))
FormEntry = get_model(*FORM_ENTRY_MODEL.split('.'))
FieldEntry = get_model(*FIELD_ENTRY_MODEL.split('.'))


class FormModelTest(TestCase):
    def test_simple_form_model(self):
        form = Form.objects.create(title='Title')

        self.assertEqual(form.slug, 'title')
        self.assertEqual(str(form), 'Title')


class FieldModelTest(TestCase):
    def test_simple_field_model(self):
        form = Form.objects.create(title='Title')
        field = Field.objects.create(label='Label', field_type=1, form=form)

        self.assertEqual(field.slug, 'label')
        self.assertEqual(str(field), 'Label')
        self.assertEqual(field.order, 0)

    def test_method_get_choices(self):
        form = Form.objects.create(title='Title')
        field = Field.objects.create(label='Label', field_type=4, choices='value1, value2, value3', form=form)
        choices = field.get_choices()

        self.assertEqual(list(choices), [('value1', 'value1'), ('value2', 'value2'), ('value3', 'value3')])


class FormEntryModelTest(TestCase):
    def test_simple_form_entry_model(self):
        form = Form.objects.create(title='Title')
        entry = FormEntry.objects.create(form=form)
        time_now = now()

        self.assertEqual(str(entry).split('.')[0], ('Title - %s' % time_now).split('.')[0])


class FieldEntryModelTest(TestCase):
    def test_field_entry_model(self):
        form = Form.objects.create(title='Title')
        form_entry = FormEntry.objects.create(form=form)
        field_entry = FieldEntry.objects.create(field_id=1, value='Value', entry=form_entry)

        self.assertEqual(str(field_entry), 'Title - 1')
        self.assertEqual(field_entry.order, 0)
