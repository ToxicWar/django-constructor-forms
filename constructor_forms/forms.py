# coding: utf-8
from __future__ import unicode_literals
from django import forms
from django.utils.timezone import now
from .utils import get_model, split_choices, import_object
from . import conf, fields as base_fields

FormEntry = get_model('FormEntry')
FieldEntry = get_model('FieldEntry')

#                                   #
#   Functions for flexible forms.   #
#                                   #

def _pre_initial(form, *args, **kwargs):
    pass


def _processing_arg_names(field, arg_names, field_args, *args, **kwargs):
    if 'max_length' in arg_names:
        field_args['max_length'] = 2000
    if 'choices' in arg_names:
        field_args['choices'] = field.get_choices()


def _add_css_classes(form, field, field_key, field_class, *args, **kwargs):
    css_class = field_class.__name__.lower()
    if field.required:
        css_class += ' required'
        if (field.field_type != base_fields.CHECKBOX_MULTIPLE):
            form.fields[field_key].widget.attrs['required'] = ''
    form.fields[field_key].widget.attrs['class'] = css_class
    if field.placeholder_text and not field.default:
        form.fields[field_key].widget.attrs['placeholder'] = field.placeholder_text


def _post_initial(form, *args, **kwargs):
    pass


pre_initial = import_object(conf.FORM_PRE_INITIAL)
processing_arg_names = import_object(conf.FORM_PROCESSING_ARG_NAMES)
add_css_classes = import_object(conf.FORM_ADD_CSS_CLASSES)
post_initial = import_object(conf.FORM_POST_INITIAL)


class ConstructorForm(forms.ModelForm):
    class Meta:
        model = FormEntry
        exclude = ('creation_time', 'form')

    def __init__(self, form, *args, **kwargs):
        '''
        Dynamically add of the form fields.
        '''
        self.form = form
        self.form_fields = form.fields.all()
        initial = kwargs.pop('initial', {})
        # If a FormEntry instance to edit, stores it's field values for using as initial data.
        field_entries = {}
        if kwargs.get('instance'):
            for field_entry in kwargs['instance'].fields.all():
                field_entries[field_entry.field_id] = field_entry.value
        pre_initial(self, *args, **kwargs)  # additional actions
        super(ConstructorForm, self).__init__(*args, **kwargs)

        # Set fields for form
        for field in self.form_fields:
            field_key = field.slug
            field_class = base_fields.CLASSES[field.field_type]
            field_args = {
                'label': field.label,
                'required': field.required,
                'help_text': field.help_text,
                'widget': base_fields.WIDGETS.get(field.field_type, None)
            }
            arg_names = field_class.__init__.__func__.__code__.co_varnames
            processing_arg_names(field, arg_names, field_args, *args, **kwargs)  # processing unique arguments

            # Initial value for field, in order of preference:
            # 1. Value of field_entries
            # 2. Value from 'initial' dictionary
            # 3. Default value
            initial_val = None
            if field_entries.get(field.id):
                initial_val = field_entries[field.id]
            elif initial.get(field_key):
                initial_val = initial[field_key]
            elif field.default:
                initial_val = field.default

            if initial_val:
                if field.is_a(base_fields.CHECKBOX_MULTIPLE, base_fields.SELECT_MULTIPLE):
                    initial_val = split_choices(initial_val)
                if field.field_type == base_fields.CHECKBOX:
                    initial_val = initial_val != 'False'
                self.initial[field_key] = initial_val
            self.fields[field_key] = field_class(**field_args)

            # initial value in extra fields
            if hasattr(field_class, 'get_initial'):
                self.initial[field_key] = field_class.get_initial(*args, **kwargs)

            # Add identifying CSS classes to the field.
            add_css_classes(self, field, field_key, field_class, *args, **kwargs)

        post_initial(self, *args, **kwargs)

    def save(self, **kwargs):
        '''
        Save a FormEntry instance and assign submitted values to related FieldEntry instances for each form field.
        '''
        entry = super(ConstructorForm, self).save(commit=False)
        entry.form = self.form
        entry.creation_time = now()
        entry.save()
        entry_fields = entry.fields.values_list('field_id', flat=True)
        _entry_fields = []

        for field in self.form_fields:
            field_key = field.slug
            field_class = base_fields.CLASSES[field.field_type]
            value = self.cleaned_data[field_key]
            if isinstance(value, list):
                value = ', '.join([item.strip() for item in value])

            # get value in extra fields
            if hasattr(field_class, 'get_value'):
                value = field_class.get_value(value=value, **kwargs)

            if field.id in entry_fields:
                field_entry = entry.fields.get(field_id=field.id)
                field_entry.value = value
                field_entry.order = field.order
                field_entry.save()
            else:
                entry_field_args = {'entry': entry, 'field_id': field.id, 'value': value, 'order': field.order}
                _entry_fields.append(FieldEntry(**entry_field_args))

        if _entry_fields:
            FieldEntry.objects.bulk_create(_entry_fields)
        return entry
