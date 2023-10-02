from django.http import HttpResponse
from django.shortcuts import render  # рендеринг шаблона
from datetime import datetime  # для отображения года копирайта в подвале
from .models import Course  # получить доступ к таблице курсов
from .models import Lesson  # получить доступ к таблице уроков


# request содержит объект текущего запроса, указывать обязательно, несмотря на предупреждения
def index(request):
    # return HttpResponse('Список курсов')
    courses = Course.objects.all()  # данные всех курсов
    current_year = datetime.now().year
    return render(request, context={'courdes': courses}, template_name='index.html')


def create(request):
    return HttpResponse('Создание курса')


def delete(request, course_id):
    return HttpResponse(f'Удаление курса с id={course_id}')


def detail(request, course_id):
    # return HttpResponse(f'Описание курса с id={course_id}')
    course = Course.objects.get(id=course_id)
    lessons = Lesson.objects.filter(course=course_id)
    context = {'course': course, 'lessons': lessons}
    return render(request, 'detail.html', context)
# проверки на существование записи нет?
# переход по http://127.0.0.1:8000/courses/detail/4000/ при наличии кусов с id = 1,2 и 3 ошибку не вызывает


def enroll(request, course_id):
    return HttpResponse(f'Запись на курс с id={course_id}')
