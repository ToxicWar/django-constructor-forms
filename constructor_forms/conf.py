# coding: utf-8
from __future__ import unicode_literals
from django.conf import settings

#                      #
#   Models settings.   #
#                      #

# Model form inherited from AbstractForm.
FORM_MODEL = getattr(settings, 'CONSTRUCTOR_FORMS_FORM_MODEL', 'constructor_forms.Form')

# Model field inherited from AbstractField.
FIELD_MODEL = getattr(settings, 'CONSTRUCTOR_FORMS_FIELD_MODEL', 'constructor_forms.Field')

# Model form entry inherited from AbstractFormEntry.
FORM_ENTRY_MODEL = getattr(settings, 'CONSTRUCTOR_FORMS_FORM_ENTRY_MODEL', 'constructor_forms.FormEntry')

# Model field entry inherited from AbstractFieldEntry.
FIELD_ENTRY_MODEL = getattr(settings, 'CONSTRUCTOR_FORMS_FIELD_ENTRY_MODEL', 'constructor_forms.FieldEntry')


#                      #
#   Fields settings.   #
#                      #

# Dictionary to modify widgets for basic fields.
MODIFICATION_WIDGETS = getattr(settings, 'CONSTRUCTOR_FORMS_MODIFICATION_WIDGETS', {})

# Additional custom fields.
EXTRA_FIELDS = getattr(settings, 'CONSTRUCTOR_FORMS_EXTRA_FIELDS', ())


#                    #
#   Form settings.   #
#                    #

# Form ConstructorForm.
CONSTRUCTOR_FORM = getattr(settings, 'CONSTRUCTOR_FORMS_CONSTRUCTOR_FORM', 'constructor_forms.forms.ConstructorForm')

# Pre initial function.
FORM_PRE_INITIAL = getattr(settings, 'CONSTRUCTOR_FORMS_FORM_PRE_INITIAL', 'constructor_forms.forms._pre_initial')

# Function processing arg names for added field arguments.
FORM_PROCESSING_ARG_NAMES = getattr(settings, 'CONSTRUCTOR_FORMS_FORM_PROCESSING_ARG_NAMES',
                                    'constructor_forms.forms._processing_arg_names')

# Function for adding css classes in form.
FORM_ADD_CSS_CLASSES = getattr(settings, 'CONSTRUCTOR_FORMS_FORM_ADD_CSS_CLASSES',
                               'constructor_forms.forms._add_css_classes')

# Post initial function.
FORM_POST_INITIAL = getattr(settings, 'CONSTRUCTOR_FORMS_FORM_POST_INITIAL', 'constructor_forms.forms._post_initial')
