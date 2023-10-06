# Структура данных приложения
from django.contrib.auth.models import AbstractUser
from django.db import models
from .fuctions import get_timestamp_path_user


# Create your models here.
class User(AbstractUser):  # Таблица пользователей на основе готового класса AbstractUser
    email = models.EmailField(unique=True, verbose_name='Email')
    birthday = models.DateField(verbose_name='Дата рождения', blank=False)
    description = models.TextField(verbose_name='Обо мне', null=True, blank=True, default='', max_length=150)
    avatar = models.ImageField(verbose_name='Фото', blank=True, upload_to=get_timestamp_path_user)
    # instance? filename?

    USERNAME_FIELD = 'email'  # Параметр- Указание поля, используемого для авторизации, т.е. логин=эл.почта
    REQUIRED_FIELDS = ['username', 'birthday']  # Список имен полей для создания суперпользователя

    class Meta:  # Свойства таблицы
        verbose_name_plural = 'Участники'  # имя записи в множ.числе
        verbose_name = 'Участник'  # Имя записи в ед.числе
        ordering = ['last_name']  # сортировка

    def __str__(self):
        return f'Участник {self.first_name} {self.last_name}: {self.email}'
