# coding: utf-8
from __future__ import unicode_literals
from django.test import TestCase
from django.utils.timezone import now
from ..utils import get_model
from .. import fields


Form = get_model('Form')
Field = get_model('Field')
FormEntry = get_model('FormEntry')
FieldEntry = get_model('FieldEntry')


class FormModelTest(TestCase):
    def test_simple_form_model(self):
        form = Form.objects.create(title='Title')

        self.assertEqual(form.slug, 'title')
        self.assertEqual(str(form), 'Title')


class FieldModelTest(TestCase):
    def test_simple_field_model(self):
        form = Form.objects.create(title='Title')
        field = Field.objects.create(label='Label', field_type=fields.TEXT, form=form)

        self.assertEqual(field.slug, 'label')
        self.assertEqual(str(field), 'Label')
        self.assertEqual(field.order, 0)

    def test_method_get_choices(self):
        form = Form.objects.create(title='Title')
        field = Field.objects.create(label='Label', field_type=fields.CHECKBOX, choices='value1, value2, value3', form=form)
        choices = field.get_choices()

        self.assertEqual(list(choices), [('value1', 'value1'), ('value2', 'value2'), ('value3', 'value3')])

    def test_is_a_method(self):
        form = Form.objects.create(title='Title')
        field = Field.objects.create(label='Label', field_type=fields.TEXT, form=form)

        self.assertTrue(field.is_a(fields.TEXT))
        self.assertFalse(field.is_a(fields.EMAIL))
        self.assertFalse(field.is_a(fields.DATE, fields.EMAIL))

    def test_delete_method(self):
        form = Form.objects.create(title='Title')
        field1 = Field.objects.create(label='Field 1', field_type=fields.TEXT, form=form)
        field2 = Field.objects.create(label='Field 2', field_type=fields.TEXT, form=form)
        field3 = Field.objects.create(label='Field 3', field_type=fields.TEXT, form=form)
        field2.delete()
        order_list = list(form.fields.values_list('order', flat=True))
        right_order_list = [0, 1]

        self.assertListEqual(order_list, right_order_list)
        self.assertEqual(form.fields.all()[1].label, 'Field 3')


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
