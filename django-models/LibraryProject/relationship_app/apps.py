from django.apps import AppConfig


class RelationshipAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relationship_app'

    def ready(self):
        import relationship_app.signals 

from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'your_app'

    def ready(self):
        import your_app.signals  # Replace 'your_app' with the correct name



# apps.py
from django.apps import AppConfig

class RelationshipAppConfig(AppConfig):
    name = 'relationship_app'

    def ready(self):
        import relationship_app.signals
