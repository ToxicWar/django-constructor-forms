# coding: utf-8
from __future__ import unicode_literals
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module


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


def import_class(import_path):
    try:
        dot = import_path.rindex('.')
    except ValueError:
        raise ImproperlyConfigured("%s isn't a Python path." % import_path)
    module, classname = import_path[:dot], import_path[dot + 1:]
    try:
        mod = import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                   (module, e))
    try:
        return getattr(mod, classname)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" class.' % (module, classname))
