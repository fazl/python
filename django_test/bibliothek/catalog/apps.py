from django.apps import AppConfig

# This class needs to be registered in the project's settings.py
# Its fully scoped name is catalog.apps.CatalogConfig
class CatalogConfig(AppConfig):
    name = 'catalog'
