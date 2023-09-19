from django.db import models
from django.conf import settings
# Create your models here.


class Course(models.Model):  # Таблица курсов
    id = models.AutoField
    title = models.CharField(verbose_name='Название курса', max_length=30, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Автор курса')
    # from django.conf import settings  (AUTH_USER_MODEL)
    description = models.TextField(verbose_name='Описание курса', max_length=200)
    # было уникальным в видео, обычным в пдф
    start_date = models.DateField(verbose_name='Старт курса')
    duration = models.PositiveIntegerField(verbose_name='Продолжительность')
    price = models.PositiveIntegerField(verbose_name='Цена', blank=True, default=0)
    count_lessons = models.PositiveIntegerField(verbose_name='Кол-во уроков')

    class Meta:
        verbose_name_plural = 'Курсы'
        verbose_name = 'Курс'
        ordering = ['title']

    def __str__(self):  # Настройка представления по умолчанию
        # - что показывать в таблице, если в learning/admin.py
        # не переопределены списки полей
        # @admin.register(Course)...
        return f'{self.title}: Старт {self.start_date}'



class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    name = models.CharField(verbose_name='Название урока', max_length=25, unique=True)
    preview = models.TextField(verbose_name='Описание урока', max_length=100)

    class Meta:
        verbose_name_plural = 'Уроки'
        verbose_name = 'Урок'
        ordering = ['course']

    def __str__(self):
        return f'{self.course}: Урок {self.name}'


class Tracking(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT, verbose_name='Урок')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Ученик')
    passed = models.BooleanField(default=None, verbose_name='Курс пройден')

    class Meta:
        ordering = ['-user']
