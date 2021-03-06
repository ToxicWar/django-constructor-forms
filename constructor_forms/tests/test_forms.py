# coding: utf-8
from __future__ import unicode_literals
from django.test import TestCase
from ..conf import CONSTRUCTOR_FORM
from ..fields import NAMES, TEXT, TEXTAREA, EMAIL, CHECKBOX, CHECKBOX_MULTIPLE
from ..utils import import_object, get_model

Form = get_model('Form')
Field = get_model('Field')
FormEntry = get_model('FormEntry')
FieldEntry = get_model('FieldEntry')
ConstructorForm = import_object(CONSTRUCTOR_FORM)


class ConstructorFormTest(TestCase):
    def create_test_forms(self):
        form = Form.objects.create(title='Test title')
        form.fields.create(label='field', field_type=TEXT)
        form.fields.create(label='text', field_type=TEXTAREA)
        form.fields.create(label='email', field_type=EMAIL)
        return form

    def test_display_form_fields(self):
        form = Form.objects.create(title='Title')
        for type, label in NAMES:
            form.fields.create(label=unicode(label), field_type=type)
        right_fields = ['single_line_text', 'multi_line_text', 'email', 'check_box', 'check_boxes', 'select',
                        'multi_select', 'radio_buttons', 'date', 'datetime', 'hidden', 'number']
        constructor_form = ConstructorForm(form=form)
        template = constructor_form.as_p()

        self.assertEqual(constructor_form.fields.keys(), right_fields)
        for field in right_fields:
            try:
                self.assertTrue(template.find('id="id_%s"' % field) != -1)
            except AssertionError:
                self.assertTrue(template.find('id="id_%s_0"' % field) != -1)

    def test_display_form_with_instance(self):
        form = self.create_test_forms()
        data = {'field': 'Test', 'text': 'Test Test', 'email': 'test@example.com'}
        ConstructorForm(form=form, data=data).save()  # created test form entry
        entry = FormEntry.objects.get()
        constructor_form = ConstructorForm(form=form, instance=entry)
        template = constructor_form.as_p()

        self.assertTrue(template.find('value="Test"') != -1)
        self.assertTrue(template.find('Test Test') != -1)
        self.assertTrue(template.find('value="test@example.com"') != -1)

    def test_display_form_with_initial_data(self):
        form = Form.objects.create(title='Title')
        form.fields.create(label='field', field_type=TEXT)
        initial = {'field': 'Some text'}
        constructor_form = ConstructorForm(form=form, initial=initial)
        template = constructor_form.as_p()

        self.assertTrue(template.find('value="Some text"') != -1)

    def test_display_form_with_default(self):
        form = Form.objects.create(title='Title')
        form.fields.create(label='field', field_type=TEXT, default='Default value')
        constructor_form = ConstructorForm(form=form)
        template = constructor_form.as_p()

        self.assertTrue(template.find('value="Default value"') != -1)

    def test_display_form_with_required_field(self):
        form = Form.objects.create(title='Title')
        form.fields.create(label='field', field_type=TEXT, required=True)
        constructor_form = ConstructorForm(form=form)
        template = constructor_form.as_p()

        self.assertTrue(template.find('class="charfield required"') != -1)

    def test_display_form_with_placeholder_text(self):
        form = Form.objects.create(title='Title')
        form.fields.create(label='field', field_type=TEXT, placeholder_text='Enter the text')
        constructor_form = ConstructorForm(form=form)
        template = constructor_form.as_p()

        self.assertTrue(template.find('placeholder="Enter the text"') != -1)

    def test_save_form(self):
        form = self.create_test_forms()
        data = {
            'field': 'Test one line',
            'text': 'Test \n Text',
            'email': 'test@example.com'
        }
        constructor_form = ConstructorForm(form=form, data=data)
        constructor_form.save()
        entry_count = FormEntry.objects.count()
        entry1, entry2, entry3 = FieldEntry.objects.all()

        self.assertEqual(entry_count, 1)
        self.assertEqual(entry1.value, 'Test one line')
        self.assertEqual(entry2.value, 'Test \n Text')
        self.assertEqual(entry3.value, 'test@example.com')

    def test_save_values_with_list(self):
        form = self.create_test_forms()
        form.fields.create(label='select', field_type=CHECKBOX_MULTIPLE, choices='val1, val2, val3')
        data = {
            'field': 'Test one line',
            'text': 'Test \n Text',
            'email': 'test@example.com',
            'select': ['val1', 'val3']
        }
        constructor_form = ConstructorForm(form=form, data=data)
        constructor_form.save()
        entry_count = FormEntry.objects.count()
        entry1 = FieldEntry.objects.get(field_id=CHECKBOX)

        self.assertEqual(entry_count, 1)
        self.assertEqual(entry1.value, 'val1, val3')

    def test_save_with_instance(self):
        form = self.create_test_forms()
        data = {'field': 'Test', 'text': 'Test Test', 'email': 'test@example.com'}
        ConstructorForm(form=form, data=data).save()  # created test form entry
        entry = FormEntry.objects.get()
        values_old = list(entry.fields.values_list('value', flat=True))

        self.assertListEqual(values_old, ['Test', 'Test Test', 'test@example.com'])

        data = {'field': 'Data', 'text': 'Data Test', 'email': 'data@example.com'}
        constructor_form = ConstructorForm(form=form, instance=entry, data=data)
        constructor_form.save()
        values_new = list(entry.fields.values_list('value', flat=True))

        self.assertListEqual(values_new, ['Data', 'Data Test', 'data@example.com'])
