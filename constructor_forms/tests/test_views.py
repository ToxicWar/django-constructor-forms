# coding: utf-8
from __future__ import unicode_literals
from django import get_version
from django.core.urlresolvers import reverse_lazy
from django.test import TestCase
from ..utils import get_model
from .. import fields

Form = get_model('Form')
Field = get_model('Field')


class FormDetailTest(TestCase):
    def setUp(self):
        self.form = Form.objects.create(title='Title')
        self.field = Field.objects.create(label='Label', field_type=fields.TEXT, form=self.form)

    def test_form_detail_view_200(self):
        version = get_version()
        # Django 1.4.10: Reverse for ''FormDetail'' with arguments '(u'title',)' and keyword arguments '{}' not found.
        if version != '1.4.10':
            response = response = self.client.get(reverse_lazy('FormDetail', kwargs={'slug': self.form.slug}))

            self.assertEqual(response.status_code, 200)

    def test_form_detail_view_404(self):
        response = self.client.get(reverse_lazy('FormDetail', kwargs={'slug': 'some-slug'}))

        self.assertEqual(response.status_code, 404)

    def test_form_detail_view_302(self):
        data = {'field': 'Test'}
        response = self.client.post(reverse_lazy('FormDetail', kwargs={'slug': self.form.slug}), data=data)

        self.assertEqual(response.status_code, 302)


class FormSentTest(TestCase):
    def setUp(self):
        self.form = Form.objects.create(title='Title')
        self.field = Field.objects.create(label='Label', field_type=fields.TEXT, form=self.form)

    def test_form_sent_view_200(self):
        response = self.client.get(reverse_lazy('FormSent', kwargs={'slug': self.form.slug}))

        self.assertEqual(response.status_code, 200)

    def test_form_sent_view_404(self):
        response = self.client.get(reverse_lazy('FormSent', kwargs={'slug': 'some-slug'}))

        self.assertEqual(response.status_code, 404)
