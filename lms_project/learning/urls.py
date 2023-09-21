from django.urls import path
from django.urls import re_path  # аналогично path, но позволяет регулярные выражения
from .views import *

# список маршрутов. имя фиксированное
# (шаблон пути, контроллер или вложенный список маршрутов)
# представления для этих путей см. во views.py

urlpatterns = [
    path('', index, name='index'),
    # Т.е при переходе в корень сайта (http://127.0.0.1:8000/) отдавать страницу index
    path('create/', create, name='create'),
    re_path('^delete/(?P<course_id>[4-9]*)/$', delete, name='delete'),
    # удалить можно будет только курсы с id от 4 до 9 - это работает
    path('detail/<int:course_id>/', detail, name='detail'),
    path('enroll/<int:course_id>/', enroll, name='enroll'),
]
# Параметр name=... позволяет применять обратный поиск адресов (по имени маршрута формируется адрес)
# <int:course_id> - параметр, передаваемый контроллеру (тип:имя).
# course_id - имя ключа в таблице курсов КОТОРОЕ НАМ из джанги НЕ ВИДНО!!!
# а в MySQL таблица называется learning_course, а поле - id!!!