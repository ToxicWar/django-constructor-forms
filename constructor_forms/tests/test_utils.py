# coding: utf-8
from __future__ import unicode_literals
from django.test import TestCase
from django.db.models import get_model
from ..conf import FORM_MODEL
from ..utils import unique_slug

Form = get_model(*FORM_MODEL.split('.'))


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
