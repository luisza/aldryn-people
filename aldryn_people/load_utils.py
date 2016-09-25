# encoding: utf-8

'''
Free as freedom will be 8/9/2016

@author: luisza
'''

from __future__ import unicode_literals
try:
    # Python>=2.7
    from importlib import import_module
except ImportError:
    # Python==2.6
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from django.utils.importlib import import_module

# otherwise it is a pain, but thanks to solution of getting model from
# https://github.com/django-oscar/django-oscar/commit/c479a1
# we can do almost the same thing from the different side.
from django.apps import apps
from django.apps.config import MODELS_MODULE_NAME
from django.core.exceptions import AppRegistryNotReady


def get_model(app_label, model_name):
    """
    Fetches a Django model using the app registry.
    This doesn't require that an app with the given app label exists,
    which makes it safe to call when the registry is being populated.
    All other methods to access models might raise an exception about the
    registry not being ready yet.
    Raises LookupError if model isn't found.
    """
    try:
        return apps.get_model(app_label, model_name)
    except AppRegistryNotReady:
        if apps.apps_ready and not apps.models_ready:
            # If this function is called while `apps.populate()` is
            # loading models, ensure that the module that defines the
            # target model has been imported and try looking the model up
            # in the app registry. This effectively emulates
            # `from path.to.app.models import Model` where we use
            # `Model = get_model('app', 'Model')` instead.
            app_config = apps.get_app_config(app_label)
            # `app_config.import_models()` cannot be used here because it
            # would interfere with `apps.populate()`.
            import_module('%s.%s' % (app_config.name, MODELS_MODULE_NAME))
            # In order to account for case-insensitivity of model_name,
            # look up the model through a private API of the app registry.
            return apps.get_registered_model(app_label, model_name)
        else:
            # This must be a different case (e.g. the model really doesn't
            # exist). We just re-raise the exception.
            raise
