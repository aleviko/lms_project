from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.models import Group  #, Permission
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.conf import settings
from datetime import datetime
from .models import User
from .forms import LoginForm, RegisterForm

# Create your views here.
# request содержит объект текущего запроса, указывать обязательно, несмотря на предупреждения


class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'login.html'
    next_page = 'index'

    def form_valid(self, form):
        is_remember = self.request.POST.get('is_remember')  # состояние галочки в отправляемой форме
        if is_remember == 'on':  # т.е. не True/False, а 'on'/'off'
            self.request.session[settings.REMEMBER_KEY] = datetime.now().isoformat()  # запоминаем в REMEMBER_KEY момент первого взведение галочки
            self.request.session.set_expiry(settings.REMEMBER_AGE)  # задаем время жизни сессии
            # в итоге нас будут помнить ~год с последнего логина
        elif is_remember == 'off':
            self.request.session.set_expiry(0)  # сессия существует до закрытия браузера
        return super(UserLoginView, self).form_valid(form)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        # имя пользователя нельзя оставлять пустым. как без этого обходятся другие?
        user.username = user.email  # насчет ширины полей вопрос так и не решен тоже
        user.save()
        # pupil = Group.objects.filter(name='Ученики')  # нового юзера автоматом добавим в группу "Ученики"
        # user.groups.set(pupil)
        # назначение прав теперь по сигналу
        dj_login(self.request, user)
        return redirect('index')

#
#
# def login(request):
#     if request.method == 'POST':
#         # получаем данные из полей формы логина и получаем запись из модели user для входящего пользователя
#         data = request.POST
#         '''Не учтен вариант принудительного захода на http://127.0.0.1:8000/auth/login/ и повторного логина
#         уже залогиненного пользователя. Попробовать:
#         if request.user.is_authenticated:
#             return HttpResponse('Вы уже вошли в систему, нет смысла делать это повторно.')'''
#         user1 = authenticate(request, email=data['email'], password=data['password'])
#         if user1 is not None and user1.is_active:  # пользователь найден (non none) и не заблокирован
#             dj_login(request, user1)  # вход пользователя - тут ругается: login() takes 1 positional argument but 2 were given
#             return redirect('index')  # перенаправляем пользователя на главную страницу
#         else:
#             if user1:
#                 return HttpResponse('Ваша учетная запись заблокирована!')
#             else:
#                 return HttpResponse('Неправильное имя или пароль')
#     else:
#         return render(request, 'login.html')  # выдаем пустую форму для входа
#
#
# def register(request):
#     if request.method == 'POST':
#         try:  # защита от падений при повторных регистрациях с одинаковым логином
#             data = request.POST
#             # объект класса model.User - все поля, кроме пароля, тянем напрямую из формы
#             user = User(email=data['email'], first_name=data['first_name'], last_name=data['last_name'],
#                         birthday=data['birthday'], description=data['description'],
#                         #avatar=data['avatar'], # ...однако аватар так не сохраняется
#                         username=data['email'])  # username достался нам в наследство от AbstractUser, он уникальный и непустой, обязателен к заполнению?
#             # пока заполняю его эл.почтой, но впереди маячит сюрприз: эл.почта длиной 256символов, а юзернейм - только 150...
#             user.set_password(data['password'])  # пароль сразу преобразуется в хэш
#             try:  # обход невыбранной/кривой/вообщеНЕ картинки без вникания в подробности. Иначе юзер без аватары не регистрируется
#                 user.avatar = request.FILES['avatar'] ### возможно, костыль, но с ним аватар сохраняется, а без него - нет. Увидено на https://qna.habr.com/q/71870
#             except:
#                 pass  # до 20231015 при незаполненной аватаре user.avatar = request.FILES['avatar'] не давал зарегать юзера
#             user.save()  # сохранение записи пользователя
#             pupil = Group.objects.filter(name='Ученики')  # нового юзера автоматом добавим в группу "Ученик"
#             # Вообще-то прописывание значений из изменяемых справочников в виде констант в коде культурные люди называют говнокодом, конкретно 1С-овской разновидности :)
#             user.groups.set(pupil)
#             dj_login(request, user)  # вход пользователя
#             return redirect('index')
#         except:
#             return HttpResponse('То ли такой юзер уже существует, то ли еще какая напасть. Разрабу было лом прояснять подробнее :)')
#     else:
#         return render(request, 'register.html')  # на запрос GET возвращаем пустую форму для регистрации
#     # return HttpResponse('Страница для <b>регистрации</b> пользователя на сайте')
#

def logout(request):
    dj_logout(request)
    return redirect('login')
    # return HttpResponse('Это представление выполняет <b>выход</b> и редирект на страницу входа')


def change_password(request):
    return HttpResponse('Обработчик изменения <b>пароля</b> пользователя')


def reset_password(request):
    return HttpResponse('Обработчик сброса <b>пароля</b> пользователя')
