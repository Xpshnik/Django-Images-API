from django.apps import AppConfig


class ImagesApiConfig(AppConfig):
    name = 'images_api'

    def ready(self):
        import images_api.signals
