from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class Exporter:
    """Object responsible of exporting fields from a given model."""

    def __init__(self, model=None, fields=None):
        self._model = model or self._get_model("EXPORTS_MODEL")
        self._fields = fields or getattr(settings, "EXPORTS_FIELDS")
        if not isinstance(self._fields, list):
            raise ImproperlyConfigured(
                "EXPORTS_FIELDS must be a list of strings."
            )
        self._order = fields or getattr(settings, "EXPORTS_ORDER",['?'])
        if not isinstance(self._order, list):
            raise ImproperlyConfigured(
        "EXPORTS_ORDER must be a list of strings."
        )

    @property
    def raw_data(self):
        """The raw data from the database."""
        return list(
            self._model.objects.order_by(*self._order).values(*self._fields)
        )

    def _merge(self, source, destination):
        """Merges recursively two dictionaries."""
        for key, value in source.items():
            if isinstance(value, dict):
                node = destination.setdefault(key, {})
                self._merge(value, node)
            else:
                destination[key] = value
        return destination

    def _build_exports(self, data):
        """Build exported data structure from raw data from database."""
        exports = []
        for element in (data):
            export = {}
            for key, value in element.items():
                parts = key.split("__")
                # recursively construct the embeded dicts data structure
                for part in reversed(parts):
                    value = {part: value}
                export = self._merge(export, value)
            exports.append(export)
            print(exports)
        return exports

    def _get_model(self, constant_name):
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

    @property
    def data(self):
        """The data to export."""
    
        return self._build_exports(self.raw_data)
     
