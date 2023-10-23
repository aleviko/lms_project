from django.contrib.auth.decorators import login_required, permission_required  # перенаправление на LOGIN_URL, проверка наличия прав
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin  # добавки с доп.функционалом
# LoginRequiredMixin - аналог декоратора login_required? PermissionRequiredMixin - ...
from django.http import HttpResponse
from django.shortcuts import render  # рендеринг шаблона
from django.shortcuts import redirect  # переадресация на заданную страницу
from django.views.generic import ListView  # извлекает набор записей из таблицы в контекстные переменные для последующей вставки шаблон
from django.views.generic import DetailView  # извлекает одну запись из таблицы в контекстные переменные для последующей вставки шаблон
# имя шаблона должно оканчиваться на "_detail"
from django.views.generic import CreateView, UpdateView, DeleteView  #
#from django.urls.base import reverse  # в уроке 7 этого нет, но без него реверс валит в ошибку
from django.shortcuts import reverse  # появилось в уроке 8
from datetime import datetime  # для отображения года копирайта в подвале
from .models import Course  # получить доступ к таблице курсов
from .models import Lesson  # получить доступ к таблице уроков
from .models import Tracking  # получить доступ к таблице записей на курсы
# request содержит объект текущего запроса, указывать обязательно, несмотря на предупреждения
from .forms import CourseForm  # классы генерации форм

class MainView(ListView):  # список курсов
    # доступ всем
    template_name = 'index.html'  # генерируемый шаблон
    queryset = Course.objects.all()  # результаты запроса
    context_object_name = 'courses'  # имя контекстной переменной, используемой в шаблоне
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['current_year'] = datetime.now().year
        return context

class CourseCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'create.html'
    model = Course
    form_class = CourseForm
    permission_required = ('learning.add_course',)  # доступ только при наличии прав learning.add_course

    def get_success_url(self):
        return reverse('detail', kwargs={'course_id': self.object.id})

    def form_valid(self, form):  # если содержимое формы прошло валидацию...
        course = form.save(commit=False)
        course.author = self.request.user
        course.save()  # ...автор дописывается поверх незакоммиченной записи
        return super(CourseCreateView, self).form_valid(form)

class CourseUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'create.html'
    model = Course
    form_class = CourseForm
    pk_url_kwarg = 'course_id'
    permission_required = ('learning.change_course',)  # доступ только при наличии прав learning.change_course

    def get_queryset(self):
        return Course.objects.filter(id=self.kwargs.get('course_id'))

    def get_success_url(self):
        return reverse('detail', kwargs={'course_id': self.object.id})


class CourseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'delete.html'
    model = Course
    pk_url_kwarg = 'course_id'
    permission_required = ('learning.delete_course',)  # доступ только при наличии прав learning.delete_course'
    # незалогинненных перенаправляет на логин, бесправным выдает 403 Forbidden


    def get_queryset(self):
        return Course.objects.filter(id=self.kwargs.get('course_id'))
    def get_success_url(self):
        return reverse('index')

class CourseDetailView(DetailView):
    template_name = 'detail.html'
    context_object_name = 'course'
    pk_url_kwarg = 'course_id'  # указываем, как называется первичный ключ


    def get_queryset(self):
        return Course.objects.filter(id=self.kwargs.get('course_id'))


    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['lessons'] = Lesson.objects.filter(course=self.kwargs.get('course_id'))
        return context


@login_required
@permission_required('learning.add_tracking', raise_exception=True)
def enroll(request, course_id):
    '''    if request.user.is_anonymous:
        return redirect('login')  # если не авторизован, то редирект на обработчик входа из auth_app
    else:
        # Проверка: не записан ли уже пользователь на этот курс
        теперь это решается @permission_required('learning.add_tracking', raise_exception=True)'''

        # тут косяк: Tracking надо фильтровать еще и по курсу!!!'''
    is_existed = Tracking.objects.filter(user=request.user, lesson__course=course_id).exists()
    if is_existed:
    # print(len(already_enrolled))
    # if len(already_enrolled) > 0:
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
