from django.apps import AppConfig


class OperationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Operations'

    def ready(self):
        import Operations.signals
        return super().ready()

