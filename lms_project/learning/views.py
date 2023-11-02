from django.contrib.auth.decorators import login_required, permission_required  # перенаправление на LOGIN_URL, проверка наличия прав
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin  # добавки с доп.функционалом
# LoginRequiredMixin - аналог декоратора login_required? PermissionRequiredMixin - ...
from django.core.exceptions import NON_FIELD_ERRORS  # сообщения об ошибках заполнения формы в общем по форме
from django.http import HttpResponse
from django.shortcuts import render  # рендеринг шаблона
from django.shortcuts import redirect  # переадресация на заданную страницу
from django.views.generic import ListView  # извлекает набор записей из таблицы в контекстные переменные для последующей вставки шаблон
from django.views.generic import DetailView  # извлекает одну запись из таблицы в контекстные переменные для последующей вставки шаблон
# имя шаблона должно оканчиваться на "_detail"
from django.db import transaction
from django.views.generic import CreateView, UpdateView, DeleteView  #
# from django.urls.base import reverse # в уроке 7 этого нет, но без него реверс валит в ошибку
from django.shortcuts import reverse  # появилось в уроке 8
from datetime import datetime  # для отображения года копирайта в подвале
from .models import Course  # получить доступ к таблице курсов
from .models import Lesson  # получить доступ к таблице уроков
from .models import Tracking, Review
# request содержит объект текущего запроса, указывать обязательно, несмотря на предупреждения
from .forms import CourseForm, ReviewForm, LessonForm  # классы генерации форм


class MainView(ListView):  # список курсов
    # доступ всем
    template_name = 'index.html'  # генерируемый шаблон
    queryset = Course.objects.all()  # результаты запроса
    context_object_name = 'courses'  # имя контекстной переменной, используемой в шаблоне
    paginate_by = 50  # переход по страницам еще не реализован, поэтому заведомо с запасом

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
        with transaction.atomic:  # оба save - в одну транзакцию
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
    permission_required = ('learning.delete_course',)  # доступ только при наличии прав learning.delete_course
    # незалогинненных перенаправляет на логин, бесправным выдает 403 Forbidden

    def get_queryset(self):
        return Course.objects.filter(id=self.kwargs.get('course_id'))

    def get_success_url(self):
        return reverse('index')


class CourseDetailView(ListView):  # было CourseDetailView(DetailView):
    template_name = 'detail.html'
    context_object_name = 'lessons'  # было context_object_name = 'course'
    pk_url_kwarg = 'course_id'  # указываем, как называется первичный ключ

    def get_queryset(self):
        return Lesson.objects.select_related('course').filter(course=self.kwargs.get('course_id'))  # типа оптимизация,
        # чтобы выдача двух полей из одной записи не производилась двумя отдельными селектами:
        # заходим со стороны детей и за счет .select_related получаем поля родительской записи тоже
        # возможна только при связях 1:1 или 1:м
        # похоже, кеширование типа 1с-овского джангистам еще предстоит изобрести
        #return Course.objects.filter(id=self.kwargs.get('course_id'))

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        # контекстные переменные для связанных таблиц (с отбором по курсу)
        # context['lessons'] = Lesson.objects.filter(course=self.kwargs.get('course_id'))
        context['reviews'] = Review.objects.select_related('user').filter(course=self.kwargs.get('course_id'))
        #context['reviews'] = Review.objects.filter(course=self.kwargs.get('course_id'))
        return context


@login_required
@permission_required('learning.add_tracking', raise_exception=True)
@transaction.atomic  # включение атомарной транзакции конкретно для этого контроллера
def enroll(request, course_id):
    '''    if request.user.is_anonymous:
        return redirect('login')  # если не авторизован, то редирект на обработчик входа из auth_app
    else:
        # Проверка: не записан ли уже пользователь на этот курс
        теперь это решается @permission_required('learning.add_tracking', raise_exception=True)'''
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


@login_required  # оставлять отзывы смогут только авторизованные юзеры
@permission_required('learning.add_review', raise_exception=True)
@transaction.non_atomic_requests  # возврат к "1 операция = 1 транзакция"
def review(request, course_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)  # объект формы с данными из словаря
        if form.errors:
            errors = form.errors[NON_FIELD_ERRORS]
            return render(request, 'review.html', { 'form': form, 'errors': errors })
        if form.is_valid():
            data = form.cleaned_data  # только корректно заполненные поля
            Review.objects.create(content=data['content'],
                              course=Course.objects.get(id=course_id),
                              user=request.user)
        return redirect(reverse('detail', kwargs={'course_id': course_id}))
    else:
        form = ReviewForm()
        return render(request, 'review.html', { 'form': form })

class LessonCreateView(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Lesson
    form_class = LessonForm
    template_name = 'create_lesson.html'
    pk_url_kwarg = 'course_id'

    permission_required('learning.add_lesson', )

    def get_success_url(self):
        return reverse('detail', kwargs={'course_id': self.kwargs.get('course_id')})

    def get_form(self, form_class=None):  # для ограничения списка курсов...
        form = super(LessonCreateView, self).get_form()
        form.fields['course'].queryset = Course.objects.filter(authors=self.request.user)  #  ... текущим автором
        return form
