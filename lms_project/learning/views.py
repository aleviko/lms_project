from django.http import HttpResponse
from django.shortcuts import render  # рендеринг шаблона
from django.shortcuts import redirect  # переадресация на заданную страницу
from datetime import datetime  # для отображения года копирайта в подвале
from .models import Course  # получить доступ к таблице курсов
from .models import Lesson  # получить доступ к таблице уроков
from .models import Tracking  # получить доступ к таблице записей на курсы


# request содержит объект текущего запроса, указывать обязательно, несмотря на предупреждения
def index(request):
    # return HttpResponse('Список курсов')
    courses = Course.objects.all()  # данные всех курсов
    current_year = datetime.now().year
    return render(request, context={'courses': courses}, template_name='index.html')


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
    # if request.user.is_authenticated
    if request.user.is_anonymous:
        return redirect('login')  #если не авторизован, то редирект на обработчик входа из auth_app
    else:
        # Проверка: не записан ли уже пользователь на этот курс
        is_existed = Tracking.objects.filter(user=request.user).exists()
        if is_existed:
            return HttpResponse('Вы уже записаны на этот курс')
        else:
            # список уроков по выбранному курсу
            lessons = Lesson.objects.filter(course=course_id)
            # заготовки записей в таблицу Tracking
            records = [Tracking(lesson=lesson, user=request.user, passed=False) for lesson in lessons]
            # массовая запись заготовок в таблицу
            Tracking.objects.bulk_create(records)
            return HttpResponse('Запись на курс прошла успешно')
            # return HttpResponse(f'Запись на курс с id={course_id}')
