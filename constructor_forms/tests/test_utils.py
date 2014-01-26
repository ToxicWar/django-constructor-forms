# coding: utf-8
from __future__ import unicode_literals
from django.test import TestCase
from ..utils import unique_slug, get_model
from ..models import Form as _Form, Field as _Field, FieldEntry as _FieldEntry, FormEntry as _FormEntry

Form = get_model('Form')


class UniqueSlugTest(TestCase):
    def test_simple_use_unique_slug(self):
        slug = unique_slug(Form.objects, 'slug', 'unique')

        self.assertEqual(slug, 'unique')

    def test_average_use_unique_slug(self):
        form = Form.objects.create(title='Title', slug='unique')
        slug = unique_slug(Form.objects, 'slug', 'unique')

        self.assertEqual(slug, 'unique-1')

    def test_complex_use_unique_slug(self):
        form = Form.objects.create(title='Title', slug='unique')
        form = Form.objects.create(title='Title', slug='unique-1')
        form = Form.objects.create(title='Title', slug='unique-2')
        form = Form.objects.create(title='Title', slug='unique-3')
        form = Form.objects.create(title='Title', slug='unique-4')
        slug = unique_slug(Form.objects, 'slug', 'unique')

        self.assertEqual(slug, 'unique-5')


class GetModelTest(TestCase):
    def test_get_model(self):
        Form = get_model('Form')
        Field = get_model('Field')
        FormEntry = get_model('FormEntry')
        FieldEntry = get_model('FieldEntry')
        Model = get_model('SomeForm')

        self.assertEqual(Form, _Form)
        self.assertEqual(Field, _Field)
        self.assertEqual(FormEntry, _FormEntry)
        self.assertEqual(FieldEntry, _FieldEntry)
        self.assertEqual(Model, None)
