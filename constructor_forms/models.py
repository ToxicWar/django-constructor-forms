# coding: utf-8
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.utils.timezone import now
from .conf import FORM_MODEL, FORM_ENTRY_MODEL
from .fields import NAMES
from .utils import unique_slug


#                           #
#   Basic abstract models.  #
#                           #

class AbstractForm(models.Model):
    '''
    The base model for constructing forms.
    '''

    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=300, unique=True)
    response = models.TextField(_('Response'), blank=True)
    emails_to = models.CharField(_('Address to'), blank=True, max_length=200)
    email_from = models.EmailField(_('From address'), blank=True)
    email_subject = models.CharField(_('Email subject'), max_length=200, blank=True)
    email_message = models.TextField(_('Message'), blank=True)

    class Meta:
        verbose_name = _('Form')
        verbose_name_plural = _('Forms')
        abstract = True

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        '''
        Create a unique slug from title.
        '''
        if not self.slug:
            slug = slugify(self)
            self.slug = unique_slug(self.__class__.objects, 'slug', slug)
        super(AbstractForm, self).save(*args, **kwargs)


class AbstractField(models.Model):
    '''
    The base model field.
    '''

    label = models.CharField(_('Label'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=300, blank=True, default='')
    field_type = models.IntegerField(_('Type'), choices=NAMES)
    required = models.BooleanField(_('Required'), default=False)
    choices = models.CharField(_('Choices'), max_length=1000, blank=True)
    default = models.CharField(_('Default value'), blank=True, max_length=2000)
    placeholder_text = models.CharField(_('Placeholder text'), null=True, blank=True, max_length=200)
    help_text = models.CharField(_('Help text'), blank=True, max_length=200)
    form = models.ForeignKey(FORM_MODEL, related_name='fields')
    order = models.IntegerField(_('Order'), null=True, blank=True)

    class Meta:
        verbose_name = _('Field')
        verbose_name_plural = _('Fields')
        ordering = ('order',)
        abstract = True

    def __unicode__(self):
        return self.label

    def get_choices(self):
        for choice in self.choices.split(','):
            choice = choice.strip()
            yield choice, choice


    def save(self, *args, **kwargs):
        '''
        Create a unique slug from label and setting order.
        '''
        if not self.slug:
            slug = slugify(self).replace('-', '_')
            self.slug = unique_slug(self.form.fields, 'slug', slug)

        if self.order is None:
            self.order = self.form.fields.count()
        return super(AbstractField, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        fields_after = self.form.fields.filter(order__gte=self.order)
        fields_after.update(order=models.F('order') - 1)
        super(AbstractField, self).delete(*args, **kwargs)


class AbstractFormEntry(models.Model):
    '''
    An entry submitted via constructed form.
    '''

    creation_time = models.DateTimeField(_('Date/time'))
    form = models.ForeignKey(FORM_MODEL, related_name='entries')

    class Meta:
        verbose_name = _('Form entry')
        verbose_name_plural = _('Form entries')
        abstract = True

    def __unicode__(self):
        return '%s - %s' % (self.form, self.creation_time)

    def save(self, *args, **kwargs):
        self.creation_time = now()
        return super(AbstractFormEntry, self).save(*args, **kwargs)


class AbstractFieldEntry(models.Model):
    '''
    A single field value for a form entry.
    '''

    field_id = models.IntegerField()
    value = models.CharField(max_length=2000, null=True)
    entry = models.ForeignKey(FORM_ENTRY_MODEL, related_name='fields')
    order = models.IntegerField(_('Order'), null=True, blank=True)

    class Meta:
        verbose_name = _('Form field entry')
        verbose_name_plural = _('Form field entries')
        ordering = ('order',)
        abstract = True

    def __unicode__(self):
        return '%s - %s' % (self.entry.form, self.field_id)

    def save(self, *args, **kwargs):
        if self.order is None:
            self.order = self.entry.fields.count()
        return super(AbstractFieldEntry, self).save(*args, **kwargs)


#                               #
#   Default implementations.    #
#                               #


class Form(AbstractForm):
    pass


class Field(AbstractField):
    pass


class FormEntry(AbstractFormEntry):
    pass


class FieldEntry(AbstractFieldEntry):
    pass
