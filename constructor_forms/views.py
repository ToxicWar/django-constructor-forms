# coding: utf-8
from __future__ import unicode_literals
from django.views.generic import FormView, TemplateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from .utils import get_model, get_constructor_form

Form = get_model('Form')
ConstructorForm = get_constructor_form()


class FormDetail(FormView):
    form_class = ConstructorForm
    template_name = 'constructor_forms/form_detail.html'

    # def get_context_data(self, **kwargs):
    #     pass

    def get_form_kwargs(self):
        kwargs = super(FormDetail, self).get_form_kwargs()
        form_slug = self.kwargs['slug']
        self.form = get_object_or_404(Form, slug=form_slug)
        kwargs['form'] = self.form
        return kwargs

    def get_success_url(self):
        return reverse_lazy('FormSent', kwargs={'slug': self.form.slug})

form_detail = FormDetail.as_view()


class FormSent(TemplateView):
    pass

form_sent = FormSent.as_view()
