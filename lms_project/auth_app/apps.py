from django.apps import AppConfig


class AuthAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_app'  # Путь к папке приложения относительно "папки проекта" - не понял!
    verbose_name = 'Управление авторизацией'

    def ready(self):  # обработка сигналов
        from .signals import grant_pupil_rights
