from django.contrib.auth.decorators import login_required, permission_required  # перенаправление на LOGIN_URL, проверка наличия прав
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin  # добавки с доп.функционалом
# LoginRequiredMixin - аналог декоратора login_required? PermissionRequiredMixin - ...
from django.core.exceptions import NON_FIELD_ERRORS  # сообщения об ошибках заполнения формы в общем по форме
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render  # рендеринг шаблона
from django.shortcuts import redirect  # переадресация на заданную страницу
from django.views.generic import ListView  # извлекает набор записей из таблицы в контекстные переменные для последующей вставки шаблон
from django.views.generic import DetailView  # извлекает одну запись из таблицы в контекстные переменные для последующей вставки шаблон
# имя шаблона должно оканчиваться на "_detail"
from django.db import transaction
from django.db.models import Q
from django.views.generic import CreateView, UpdateView, DeleteView, FormView  #
# from django.urls.base import reverse # в уроке 7 этого нет, но без него реверс валит в ошибку
from django.shortcuts import reverse  # появилось в уроке 8
from datetime import datetime  # для отображения года копирайта в подвале
from django.db.models.signals import pre_save
from .models import Course  # получить доступ к таблице курсов
from .models import Lesson  # получить доступ к таблице уроков
from .models import Tracking, Review
# request содержит объект текущего запроса, указывать обязательно, несмотря на предупреждения
from .forms import CourseForm, ReviewForm, LessonForm, OrderByAndSearchForm, SettingForm  # классы генерации форм
from .signals import set_views, course_enroll, get_certificate

class MainView(ListView, FormView):  # список курсов
    # доступ всем
    template_name = 'index.html'  # генерируемый шаблон
    queryset = Course.objects.all()  # результаты запроса
    context_object_name = 'courses'  # имя контекстной переменной, используемой в шаблоне
    paginate_by = 50  # переход по страницам еще не реализован, поэтому заведомо с запасом
    form_class = OrderByAndSearchForm

    def get_queryset(self):
        queryset = MainView.queryset
        if {'search', 'price_order'} != self.request.GET.keys():
            return queryset  # если не поиск и не сортировка, то вернуть все записи
        else:
            search_query = self.request.GET.get('search')
            price_order_by = self.request.GET.get('price_order')
            flt = Q(title__icontains=search_query) | Q(description__icontains=search_query)
            queryset = queryset.filter(flt).order_by(price_order_by)  # отобранные курсы отсортированные по цене
            return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['current_year'] = datetime.now().year
        return context

    def get_initial(self):
        initial = super(MainView, self).get_initial()
        initial['search'] = self.request.GET.get('search', '')
        initial['price_order'] = self.request.GET.get('price_order', 'title')
        return initial

    def get_paginate_by(self, queryset):
        return self.request.COOKIES.get('paginate_by', 5)


class CourseCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'create.html'
    model = Course
    form_class = CourseForm
    permission_required = ('learning.add_course',)  # доступ только при наличии прав learning.add_course

    def get_success_url(self):
        #return reverse('detail', kwargs={'course_id': self.object.id})
        # print(f'self.object.id={self.object.id}')
        return reverse('create_lesson', kwargs={'course_id': self.object.id})  #временно перевел стрелку, чтобы хоть так можно было добавить курс после "оптимизации" (курс без уроков приводит к ошибке)

    def form_valid(self, form):  # если содержимое формы прошло валидацию...
        with transaction.atomic():  # до return все в одной транзакции
            course = form.save()
            course.authors.add(self.request.user)  # привязка автора (authors = many:many)
            course.save()  # ...автор дописывается
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
        # return Course.objects.filter(id=self.kwargs.get('course_id'))

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        # контекстные переменные для связанных таблиц (с отбором по курсу)
        # context['lessons'] = Lesson.objects.filter(course=self.kwargs.get('course_id'))
        context['reviews'] = Review.objects.select_related('user').filter(course=self.kwargs.get('course_id'))
        # context['reviews'] = Review.objects.filter(course=self.kwargs.get('course_id'))
        return context

    def get(self, request, *args, **kwargs):
        set_views.send(sender=self.__class__, session=request.session,
                       pk_url_kwarg=CourseDetailView.pk_url_kwarg,
                       id=kwargs[CourseDetailView.pk_url_kwarg])
        # переехало в сигналы
        # views = request.session.setdefault('views', {})  # счетчик посещений страницы извлечение, если есть
        # course_id = str(kwargs[CourseDetailView.pk_url_kwarg])  # ключ страницы (а зачем в строку конвертить?)
        # count = views.get(course_id, 0)  # извлечение хранимого счетчика (если есть или 0)
        # views[course_id] = count + 1
        # request.session['views'] = views
        return super(CourseDetailView, self).get(request, *args, **kwargs)


@login_required
@permission_required('learning.add_tracking', raise_exception=True)
@transaction.atomic()  # включение атомарной транзакции конкретно для этого контроллера
def enroll(request, course_id):
    is_existed = Tracking.objects.filter(user=request.user, lesson__course=course_id).exists()
    if is_existed:
        return HttpResponse('Вы уже записаны на этот курс')
    else:
        # список уроков по выбранному курсу
        lessons = Lesson.objects.filter(course=course_id)
        # заготовки записей в таблицу Tracking
        records = [Tracking(lesson=lesson, user=request.user, passed=False) for lesson in lessons]
        # массовая запись заготовок в таблицу
        Tracking.objects.bulk_create(records)
        # отправка уведомления о подписке
        course_enroll.send(sender=Tracking, request=request, course_id=course_id)

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
            return render(request, 'review.html', {'form': form, 'errors': errors})
        if form.is_valid():
            data = form.cleaned_data  # только корректно заполненные поля
            Review.objects.create(content=data['content'], course=Course.objects.get(id=course_id), user=request.user)
        return redirect(reverse('detail', kwargs={'course_id': course_id}))
    else:
        form = ReviewForm()
        return render(request, 'review.html', {'form': form})


def add_booking(request, course_id):
    if request.method == 'POST':
        favourites = request.session.get('favourites', list())
        favourites.append(course_id)
        request.session['favourites'] = favourites
        request.session.modified = True
    return redirect(reverse('index'))


def remove_booking(request, course_id):
    if request.method == 'POST':
        request.session.get('favourites').remove(course_id)
        request.session.modified = True
    return redirect(reverse('index'))


@login_required
def get_certificate_view(request):
    get_certificate.send(sender=request.user)
    return HttpResponse('Сертификат отправлен на Ваш email')


class LessonCreateView(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Lesson
    form_class = LessonForm
    template_name = 'create_lesson.html'
    pk_url_kwarg = 'course_id'

    permission_required('learning.add_lesson', )

    def form_valid(self, form):  # принудительная отправка сигнала
        error = pre_save.send(sender=LessonCreateView.model, instance=form.save(commit=False))
        if error[0][1]:
            form.errors[NON_FIELD_ERRORS] = [error[0][1]]  # выдача ошибок, если есть, на форму
            return super(LessonCreateView, self).form_invalid(form)
        else:
            return super(LessonCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('detail', kwargs={'course_id': self.kwargs.get('course_id')})

    def get_form(self, form_class=None):  # для ограничения списка курсов...
        form = super(LessonCreateView, self).get_form()
        form.fields['course'].queryset = Course.objects.filter(authors=self.request.user)  # ... текущим автором
        return form


class FavouriteView(MainView):
    def get_queryset(self):
        queryset = super(FavouriteView, self).get_queryset()
        ids = self.request.session.get('favourites', list())
        return queryset.filter(id__in=ids)


class SettingFormView(FormView):
    form_class = SettingForm
    template_name = 'settings.html'

    def post(self, request, *args, **kwargs):
        paginate_by = request.POST.get('paginate_by')
        responce = HttpResponseRedirect(reverse('index'), 'Настройки сохранены')
        responce.set_cookie('paginate_by', value=paginate_by, secure=False, httponly=False,
                            samesite='Lax', max_age=60 * 60 * 24 * 365)
        return responce

    def get_initial(self):
        initial = super(SettingFormView, self).get_initial()
        initial['paginate_by'] = self.request.COOKIES.get('paginate_by', 5)
        return initial
