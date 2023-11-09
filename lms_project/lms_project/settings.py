"""
Django settings for lms_project project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-osmnvaebrl#9+bs-s^#6r7q8_w=wtbu)x3b=5q-_n6_2svcupe'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INTERNAL_IPS = ["127.0.0.1",]  # адреса, на обращения с к-рых будет отвечать django-debug-toolbar

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Наши приложения
    'auth_app.apps.AuthAppConfig',
    'learning.apps.LearningConfig',
    # Утилиты
    'debug_toolbar',  # django. указывать не надо и через _!

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',    # порядок важен!
    'django.middleware.common.CommonMiddleware',        # порядок важен!
    'django.middleware.cache.FetchFromCacheMiddleware',    # порядок важен!
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Утилиты
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # django. указывать не надо и через _!
]

# Настройки сессий
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'  # хранить сессии в кеше - еще быстрее
SESSION_CACHE_ALIAS = 'session_store'
# SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # хранить сессии в БД - для серьезных систем удобнее и быстрее
# SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'  # хранить сессии в кеше сервера - для макс.производительности
# SESSION_ENGINE = 'django.contrib.sessions.backends.file'  # хранить сессии в ФС - для разгрузки дохлых серверов БД
# SESSION_FILE_PATH = BASE_DIR / 'session' # папка для файлов сессий, если хранить сессии в ФС

# SESSION_EXPIRE_AT_BROWSER_CLOSE = True # бесполезно, т.к. браузер может перекрыть своими настройками
# SESSION_COOKIE_AGE = 30  # время жизни сессии в секундах (независимо от закрытия браузера и простоя) - уже полезнее, но неудобно - нужен таймаут по простою.
# И я НЕ ЗАМЕТИЛ, что работает (Firefox, запоминание учеток включено - т.е. тоже ненадежно
# полезные варианты см.: https://stackoverflow.com/questions/14830669/how-to-expire-django-session-in-5minutes

# SESSION_SAVE_EVERY_REQUEST = True
#SESSION_COOKIE_SECURE = True  # доступ к кукам только по https, при отладке должно мешать
SESSION_COOKIE_SAMESITE = 'Strict'  # запрет на отправку сторонним сайтам/'None' - разрешить всегда / 'Lax' - при переходе по ссылке

# Настройки запоминания пользователя - не встроенные параметры, а наша самодеятельность
REMEMBER_KEY = 'is_remember'  # см. auth_app/forms.py LoginForm. т.е. глобальная конфига теперь зависит от локальной формы...
REMEMBER_AGE = 60 * 60 * 24 * 365  # помнить юзера примерно год


ROOT_URLCONF = 'lms_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.csrf',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    },
]

WSGI_APPLICATION = 'lms_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'USER': os.environ.get('USER_DB'),  # 'lms_user',  # окружение барахлит, пока константой
        'PASSWORD': os.environ.get('PASSWORD_DB'),  # '111',  # окружение барахлит, пока константой
        'NAME': 'lms_db',  # назвал по-своему, утомила уже путаница в одинаковых именах
        'ATOMIC_REQUEST': True,  # заключить в транзакцию время работы контроллера
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/0',
    },
    'session_store': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 60 * 10   # время жизни кеша всего сайта, сек.
CACHE_MIDDLEWARE_PREFIX = 'codeby'  # префикс сайта в кеше, если кеш используется несколькими сайтами

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru'  # 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

SHORT_DATETIME_FORMAT = 'd.m.Y H:i:s'  # секунды почему-то не отображаются ни в какую, возможно это вообще не работает
# https://stacktuts.com/how-to-format-datetime-in-django-template


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = BASE_DIR / 'static'  # путь к папке со статическими файлами
STATIC_URL = '/static/'  # префикс URL для статических файлов
STATICFILES_DIRS = [
    BASE_DIR / 'static/img',
    BASE_DIR / 'static/styles',
    BASE_DIR / 'static/scripts',
]  # дополнительные пути для хранения статических файлов


# ## В шаблоне такой секции не было
# Media files
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # путь на стороне сервера к папке с загруженными файлами
MEDIA_ROOT = BASE_DIR / 'media' # новый вариант (а старый кто придумал?)
MEDIA_URL = '/media/'  # базовый адрес для формирования ссылок на загружаемые файлы

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'auth_app.User'  # Переопределение класса аутентификации

LOGIN_URL = 'login'  # перенаправление неавторизованного пользователя
LOGIN_REDIRECT_URL = 'index'  # перенаправление после успешной авторизации
LOGOUT_URL = 'logout'  # перенаправление после выхода пользователя с сайта

# для отправки эл.почты при восстановлении пароля
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # в консоль
EMAIL_HOST = 'smtp.jino.ru'  # SMTP сервер
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')  # 'lms@aleviko.ru'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')  # 'lms987#@GHdf'
EMAIL_USE_TLS = True  # EMAIL_USE_SSL = True
EMAIL_PORT = 587  # EMAIL_PORT = 465
DEFAULT_FROM_EMAIL = SERVER_EMAIL = EMAIL_HOST_USER  # для вставки в письма в сигналах. а напрямую чем хуже?
#SERVER_EMAIL для рассылки через send_mass_mail
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # имитация выводм в консоль
#EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"  # ...в папку
#EMAIL_FILE_PATH = "/home/a1/PycharmProjects/tmps"  # если в папку, то указывать обязательно полный абсолютный путь к папке
# список админов для рассылки через send_mass_mail - зачем оно нам сейчас? и почему не по списку юзеров?
ADMINS = [
    ('Admin1Name', 'admin1@site.fun'),
    ('Admin2Name', 'admin2@site.fun'),
]
# список менеджеров для рассылки через send_mass_mail - зачем оно нам сейчас? и почему не по списку юзеров?
MANAGERS = [
    ('Manager1Name', 'mul1@site.fun'),
    ('Manager2Name', 'mul2@site.fun'),
]




PASSWORD_RESET_TIMEOUT_DAYS = 1  # срок годности ссылки для восстановления пароля (приблизительно в сутках) - найти способ вставить его в письмо