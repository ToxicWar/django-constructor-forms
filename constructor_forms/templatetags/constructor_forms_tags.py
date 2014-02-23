# coding: utf-8
from __future__ import unicode_literals
from django import template
from django.template.loader import get_template
from ..utils import get_model, get_constructor_form

Form = get_model('Form')
ConstructorForm = get_constructor_form()

register = template.Library()


class BuiltFormNode(template.Node):
    def __init__(self, name, value, template):
        self.name = name
        self.value = value
        self.template = template

    def render(self, context):
        if self.name != 'form':
            try:
                form = Form.objects.get(**{str(self.name): template.Variable(self.value).resolve(context)})
            except Form.DoesNotExist:
                form = None
        else:
            form = template.Variable(self.value).resolve(context)

        if not isinstance(form, Form):
            return ''

        if self.template:
            t = get_template('constructor_forms/includes/%s' % self.template)
        else:
            t = get_template('constructor_forms/includes/constructor_form.html')
        context['form'] = form
        context['constructor_form'] = ConstructorForm(form)
        return t.render(context)


@register.tag
def render_constructor_form(parser, token):
    '''
    render_constructor_form takes one argument in one of the following formats:

    {% render_constructor_form form_instance %}
    {% render_constructor_form form=form_instance %}
    {% render_constructor_form slug=form_instance.slug %}
    {% render_constructor_form form_instance 'template.html' %}
    {% render_constructor_form form=form_instance template='template.html' %}
    '''
    try:
        try:
            _, arg, t = token.split_contents()
        except ValueError:
            _, arg = token.split_contents()
            t = None

        if '=' not in arg:
            arg = 'form=' + arg
        if '=' not in t:
            t = 'template=' + t
        name, value = arg.split('=', 1)
        t = t.split('=')[1].replace("'", '').replace('"', '')
        if name not in ('form', 'slug'):
            raise ValueError
    except ValueError as e:
        raise template.TemplateSyntaxError(render_constructor_form.__doc__)
    return BuiltFormNode(name, value, t)
