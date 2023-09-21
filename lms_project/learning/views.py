from django.http import HttpResponse
from django.shortcuts import render


# request содержит объект текущего запроса, указывать обязательно, несмотря на предупреждения
def index(request):
    return HttpResponse('Список курсов')


def create(request):
    return HttpResponse('Создание курса')


def delete(request, course_id):
    return HttpResponse(f'Удаление курса с id={course_id}')


def detail(request, course_id):
    return HttpResponse(f'Описание курса с id={course_id}')
# проверки на существование записи нет?
# переход по http://127.0.0.1:8000/courses/detail/4000/ при наличии кусов с id = 1,2 и 3 ошибку не вызывает


def enroll(request, course_id):
    return HttpResponse(f'Запись на курс с id={course_id}')
