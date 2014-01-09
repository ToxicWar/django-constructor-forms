# coding: utf-8
from __future__ import unicode_literals
from django.conf import settings

# Model form inherited from AbstractForm.
FORM_MODEL = getattr(settings, 'CONSTRUCTOR_FORMS_FORM_MODEL', 'constructor_forms.Form')

# Model field inherited from AbstractField.
FIELD_MODEL = getattr(settings, 'CONSTRUCTOR_FORMS_FIELD_MODEL', 'constructor_forms.Field')

# Model form entry inherited from AbstractFormEntry.
FORM_ENTRY_MODEL = getattr(settings, 'CONSTRUCTOR_FORMS_FORM_ENTRY_MODEL', 'constructor_forms.FormEntry')

# Model field entry inherited from AbstractFieldEntry.
FIELD_ENTRY_MODEL = getattr(settings, 'CONSTRUCTOR_FORMS_FIELD_ENTRY_MODEL', 'constructor_forms.FieldEntry')

# Dictionary to modify widgets for basic fields.
MODIFICATION_WIDGETS = getattr(settings, 'CONSTRUCTOR_FORMS_MODIFICATION_WIDGETS', {})

# Additional custom fields.
EXTRA_FIELDS = getattr(settings, 'CONSTRUCTOR_FORMS_EXTRA_FIELDS', ())
