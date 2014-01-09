# coding: utf-8
from __future__ import unicode_literals
from django.views.generic import FormView, TemplateView


class FormDetail(FormView):
    pass

form_detail = FormDetail.as_view()


class FormSent(TemplateView):
    pass

form_sent = FormSent.as_view()
