# coding: utf-8
from __future__ import unicode_literals
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model as _get_model
from django.utils.importlib import import_module
from .conf import FORM_MODEL, FIELD_MODEL, FORM_ENTRY_MODEL, FIELD_ENTRY_MODEL, CONSTRUCTOR_FORM


def unique_slug(manager, slug_field, slug):
    i = 0
    while True:
        if i > 0:
            if i > 1:
                slug = slug.rsplit('-', 1)[0]
            slug = '%s-%s' % (slug, i)
        if not manager.filter(**{slug_field: slug}):
            break
        i += 1
    return slug


def split_choices(choices_string):
    return filter(None, [x.strip() for x in choices_string.split(",")])


def import_object(import_path):
    try:
        dot = import_path.rindex('.')
    except ValueError:
        raise ImproperlyConfigured("%s isn't a Python path." % import_path)
    module, classname = import_path[:dot], import_path[dot + 1:]
    try:
        mod = import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured('Error importing module %s: "%s"' % (module, e))
    try:
        return getattr(mod, classname)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" class.' % (module, classname))


def get_model(model_name):
    if model_name == 'Form':
        return _get_model(*FORM_MODEL.split('.'))
    elif model_name == 'Field':
        return _get_model(*FIELD_MODEL.split('.'))
    elif model_name == 'FormEntry':
        return _get_model(*FORM_ENTRY_MODEL.split('.'))
    elif model_name == 'FieldEntry':
        return _get_model(*FIELD_ENTRY_MODEL.split('.'))
    else:
        return None


def get_constructor_form():
    return import_object(CONSTRUCTOR_FORM)
