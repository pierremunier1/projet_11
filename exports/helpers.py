from django.apps import apps as django_apps
from django.conf import settings


def get_exports(data):
    """Returns a list of dictionaries containing the instances to export."""
    model = get_model("EXPORTS_MODEL")
    fields = getattr(settings, "EXPORTS_FIELDS")
    if not isinstance(fields, list):
        raise ImproperlyConfigured(
            "EXPORTS_FIELDS must be a list of strings."
        )
    order = getattr(settings, "EXPORTS_ORDER", ['?'])
    if not isinstance(order, list):
        raise ImproperlyConfigured()
            "EXPORTS_ORDER must be a list of strings."
        )
    # raw data from the database
    data = list(model.objects.order_by(*order).values(*fields))
    # present foreign key data as embedded dictionnaries
    exports = []
    for element in data:
        export = {}
        for key, value in element.items():
            parts = key.split("__")
            # recursively construct the embeded dicts data structure
            for part in reversed(parts):
                value = {part: value}
            export = {**export, **value}
        exports.append(export)
    return exports

def get_model(self, constant_name):
    """Returns the model specified with constant_name in the settings."""
    model_name = getattr(settings, constant_name)
    try:
        return django_apps.get_model(model_name, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            f"{constant_name} must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"{constant_name} refers to model '{model_name}' "
            "that has not been installed"
        )
