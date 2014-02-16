# coding: utf-8
from __future__ import unicode_literals
from django.views.generic import FormView, TemplateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from .utils import get_model, get_constructor_form, import_object
from .conf import DETAIL_VIEW_INITIAL_KWARGS, SENT_VIEW_INITIAL_CONTEXT

Form = get_model('Form')
ConstructorForm = get_constructor_form()

#                                        #
#   Functions for flexible FormDetail.   #
#                                        #

def _initial_kwargs(view, kwargs):
    pass


def _initial_context(view, context):
    pass


initial_kwargs = import_object(DETAIL_VIEW_INITIAL_KWARGS)
initial_context = import_object(SENT_VIEW_INITIAL_CONTEXT)


class FormDetail(FormView):
    form_class = ConstructorForm
    template_name = 'constructor_forms/form_detail.html'

    def get_form_kwargs(self):
        kwargs = super(FormDetail, self).get_form_kwargs()
        form_slug = self.kwargs['slug']
        self.form = get_object_or_404(Form, slug=form_slug)
        kwargs['form'] = self.form
        initial_kwargs(self, kwargs)
        return kwargs

    def get_success_url(self):
        return reverse_lazy('FormSent', kwargs={'slug': self.form.slug})

form_detail = FormDetail.as_view()


class FormSent(TemplateView):
    template_name = 'constructor_forms/form_sent.html'

    def get_context_data(self, **kwargs):
        context = super(FormSent, self).get_context_data(**kwargs)
        context['form'] = get_object_or_404(Form, slug=self.kwargs['slug'])
        initial_context(self, context)
        return context

form_sent = FormSent.as_view()
