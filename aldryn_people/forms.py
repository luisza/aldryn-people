# encoding: utf-8

'''
Free as freedom will be 8/9/2016

@author: luisza
'''

from __future__ import unicode_literals
from django import forms
from django.conf import settings
from reversion.revisions import revision_context_manager
from django.apps import apps

from .load_utils import get_model
from .models import Person

userprofile_model = getattr(settings, 'ALDRYN_PEOPLE_PERSON_PROFILE',
                            'aldryn_people.personprofile')
userprofile_app_name, model_model = userprofile_model.split('.')
userprofile_model_object = get_model(userprofile_app_name, model_model)
from aldryn_reversion.utils import (
    build_obj_repr, get_translation_info_message,
)
from django.utils.translation import ugettext_lazy as _, ugettext
from django.db import transaction
from cms.wizards.forms import BaseFormMixin
from parler.forms import TranslatableModelForm
from collections import OrderedDict
import six


class ProfileForm(forms.ModelForm):

    class Meta:
        model = userprofile_model_object
        fields = '__all__'


class MyFormMetaClass(forms.models.ModelFormMetaclass):

    def __new__(mcs, name, bases, attrs):
        formfield_callback = attrs.get('formfield_callback', None)
        meta = attrs['Meta']
        new_class = super(MyFormMetaClass, mcs).__new__(
            mcs, name, bases, attrs)
        fields = None
        if hasattr(meta, "extra_onetoone_fields"):
            fields = meta.extra_onetoone_fields

        opts = forms.models.ModelFormOptions(getattr(new_class, 'Meta', None))
        rel_field = getattr(opts.model, meta.onetoone_model).field
        model = rel_field.rel.to

        extra_fields = forms.models.fields_for_model(
            model,
            # formfield_callback=formfield_callback, solve with relation
            fields=fields)
        new_class.base_fields.update(extra_fields)

        return new_class


class PersonForm(six.with_metaclass(MyFormMetaClass, forms.models.BaseModelForm)):

    #     def __init__(self, *args, **kwargs):
    #         # magic
    #         profile_kwargs = kwargs.copy()
    #         for wizard_field in ['wizard_user', 'wizard_page', 'wizard_language']:
    #             if wizard_field in profile_kwargs:
    #                 del profile_kwargs[wizard_field]
    #         if 'instance' in kwargs and kwargs['instance']:
    #             profile_kwargs['instance'] = kwargs['instance'].profile
    #         self.profileForm = ProfileForm(*args, **profile_kwargs)
    #         # magic end
    #
    #         if 'wizard_language' not in kwargs:
    #             kwargs['wizard_language'] = 'es'
    #         super(PersonForm, self).__init__(*args, **kwargs)
    #
    #         self.fields.update(self.profileForm.fields)
    #         self.initial.update(self.profileForm.initial)
    #         fields_order = ["name", "slug", "user", "vcard_enabled", "groups"]
    #         if getattr(settings,
    #                    'ALDRYN_PEOPLE_PERSON_PROFILE',
    #                    'aldryn_people.personprofile'
    #                    ) == 'aldryn_people.personprofile':
    #             profile_order = ["visual", "email", "description",
    #                              "phone", "mobile", "fax", "website"]
    #         else:
    #             profile_order = [
    #                 fieldname for fieldname in self.profileForm.fields]
    #
    #         fields_order += profile_order
    # #         # define fields order if needed
    #
    #         fields = self.fields
    #         self.fields = OrderedDict(
    #             [(key, fields[key]) for key in fields_order])

    def save(self, *args, **kwargs):
        # save both forms
        profile = self.profileForm.save(commit=False)

        """
        Ensure we create a revision for reversion.
        """
        person = super(PersonForm, self).save(commit=False)

        # Ensure we make an initial revision
        with transaction.atomic():
            with revision_context_manager.create_revision():
                profile.save()
                person.profile = profile
                person.save()
                self.save_m2m()
                if self.user:
                    revision_context_manager.set_user(self.user)
                object_repr = build_obj_repr(person) + build_obj_repr(profile)
                translation_info = get_translation_info_message(person)
                revision_context_manager.set_comment(
                    ugettext(
                        "Initial version of {object_repr}. {trans_info}".format(
                            object_repr=object_repr,
                            trans_info=translation_info)))
        return person

    class Meta:
        model = Person
        onetoone_model = 'profile'  # userprofile_model_object
        fields = '__all__'
        exclude = ['profile']
