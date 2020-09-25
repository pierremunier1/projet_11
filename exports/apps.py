"""Configuration module for the FavoriteCart app."""

from django.apps import AppConfig


class ExportsConfig(AppConfig):
    """Main config data structure for the exports app."""

    name = 'exports'

    def ready(self):
        """Initializations to be performed with the app is ready."""
        try:
            from . import signals
        except ImportError:
            pass
