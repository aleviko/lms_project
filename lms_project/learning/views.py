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
    return render(request, context={'courses': courses, 'current_year': current_year}, template_name='index.html')
    # context={объекты, которые хотим передать в страницу}, template_name='шаблон страницы'


def create(request):
    if request.method == 'POST':
        # если был вызов с методом POST, извлекаем данные из заполненной формы, пользователя подставляем текущего
        # и создаем новую запись
        data = request.POST
        Course.objects.create(title=data['title'],
                              author=request.user,
                              description=data['description'],
                              start_date=data['start_date'],
                              duration=data['duration'],
                              price=data['price'],
                              count_lessons=data['count_lessons']
                              )
        return redirect('index')
        # и перенаправляем пользователя на список курсов (а логичнее заставить его повводить уроки)
    else:
        # если был вызов с методом GET, создаем пустую форму для заполннения
        return render(request, 'create.html')
    #return HttpResponse('Создание курса')


def delete(request, course_id):
    Course.objects.get(id=course_id).delete()  # найти по ИД и удалить
    return redirect('index')  # и вернуть (переадресовать) на список курсов
    # return HttpResponse(f'Удаление курса с id={course_id}')


def detail(request, course_id):
    # return HttpResponse(f'Описание курса с id={course_id}')
    course = Course.objects.get(id=course_id)
    lessons = Lesson.objects.filter(course=course_id)
    context = {'course': course, 'lessons': lessons}
    return render(request, 'detail.html', context)  # позиционная передача параметров
# проверки на существование записи нет?
# переход по http://127.0.0.1:8000/courses/detail/4000/ при наличии кусов с id = 1,2 и 3 ошибку не вызывает


def enroll(request, course_id):
    # if request.user.is_authenticated
    if request.user.is_anonymous:
        return redirect('login')  # если не авторизован, то редирект на обработчик входа из auth_app
    else:
        # Проверка: не записан ли уже пользователь на этот курс
        # тут косяк: Tracing надо фильтровать еще и по курсу!!!
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
