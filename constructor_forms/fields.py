# coding: utf-8
from __future__ import unicode_literals
from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
from .conf import MODIFICATION_WIDGETS, EXTRA_FIELDS
from .utils import import_object


# Constants for base field types.
TEXT = 1
TEXTAREA = 2
EMAIL = 3
CHECKBOX = 4
CHECKBOX_MULTIPLE = 5
SELECT = 6
SELECT_MULTIPLE = 7
RADIO = 8
DATE = 9
DATE_TIME = 10
HIDDEN = 11
NUMBER = 12

# Names for base field types.
NAMES = (
    (TEXT, _('Single line text')),
    (TEXTAREA, _('Multi line text')),
    (EMAIL, _('Email')),
    (CHECKBOX, _('Check box')),
    (CHECKBOX_MULTIPLE, _('Check boxes')),
    (SELECT, _('Select')),
    (SELECT_MULTIPLE, _('Multi select')),
    (RADIO, _('Radio buttons')),
    (DATE, _('Date')),
    (DATE_TIME, _('Date/time')),
    (HIDDEN, _('Hidden')),
    (NUMBER, _('Number')),
)

# Field classes for base field types.
CLASSES = {
    TEXT: forms.CharField,
    TEXTAREA: forms.CharField,
    EMAIL: forms.EmailField,
    CHECKBOX: forms.BooleanField,
    CHECKBOX_MULTIPLE: forms.MultipleChoiceField,
    SELECT: forms.ChoiceField,
    SELECT_MULTIPLE: forms.MultipleChoiceField,
    RADIO: forms.ChoiceField,
    DATE: forms.DateField,
    DATE_TIME: forms.DateTimeField,
    HIDDEN: forms.CharField,
    NUMBER: forms.FloatField,
}

# Widgets for field types where a specialised widget is required.
WIDGETS = {
    TEXTAREA: forms.Textarea,
    CHECKBOX_MULTIPLE: forms.CheckboxSelectMultiple,
    RADIO: forms.RadioSelect,
    DATE: forms.DateInput,
    DATE_TIME: forms.DateTimeInput,
    HIDDEN: forms.HiddenInput,
}

# Some helper groupings of field types.
CHOICES = (CHECKBOX, SELECT, RADIO)
DATES = (DATE, DATE_TIME)
MULTIPLE = (CHECKBOX_MULTIPLE, SELECT_MULTIPLE)

# Modification widgets base fields.
for field_id, widget_path in MODIFICATION_WIDGETS.items():
    WIDGETS[field_id] = import_object(widget_path)

# Add custom fields.
for field_id, field_path, field_name in EXTRA_FIELDS:
    if field_id in CLASSES:
        raise ImproperlyConfigured('ID %s for field %s in FORMS_EXTRA_FIELDS already exists' % (field_id, field_name))
    CLASSES[field_id] = import_object(field_path)
    NAMES += ((field_id, _(field_name)),)
