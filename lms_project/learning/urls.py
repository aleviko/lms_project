from django.urls import path, reverse
# from django.urls import re_path  # аналогично path, но позволяет регулярные выражения
from .views import *

# список маршрутов. имя фиксированное
# (шаблон пути, контроллер или вложенный список маршрутов)
# представления для этих путей см. во views.py

urlpatterns = [
    path('',
        MainView.as_view(
        #template_name = 'index.html', queryset = Course.objects.all(),
        # context_object_name = 'courses'
        ),
        name='index'),
    path('create/', CourseCreateView.as_view(), name='create'),
    path('delete/<int:course_id>/', CourseDeleteView.as_view(), name='delete'),
    path('detail/<int:course_id>/', CourseDetailView.as_view(), name='detail'),
    path('update/<int:course_id>/', CourseUpdateView.as_view(), name='update'),
    path('enroll/<int:course_id>/', enroll, name='enroll'),
]
# Параметр name=... позволяет применять обратный поиск адресов (по имени маршрута формируется адрес)
# <int:course_id> - параметр, передаваемый контроллеру (тип:имя).
# course_id - имя ключа в таблице курсов КОТОРОЕ НАМ из джанги НЕ ВИДНО!!!
# а в MySQL таблица называется learning_course, а поле - id!!!
