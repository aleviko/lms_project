from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from .models import User

# Create your views here.
# request содержит объект текущего запроса, указывать обязательно, несмотря на предупреждения


def login(request):
    if request.method == 'POST':
        # получаем данные из полей формы логина и получаем запись из модели user для входящего пользователя
        data = request.POST
        '''Не учтен вариант принудительного захода на http://127.0.0.1:8000/auth/login/ и повторного логина
        уже залогиненного пользователя. Попробовать:
        if request.user.is_authenticated:
            return HttpResponse('Вы уже вошли в систему, нет смысла делать это повторно.')'''
        user1 = authenticate(request, email=data['email'], password=data['password'])
        if user1 is not None and user1.is_active:  # пользователь найден (non none) и не заблокирован
            dj_login(request, user1)  # вход пользователя - тут ругается: login() takes 1 positional argument but 2 were given
            return redirect('index')  # перенаправляем пользователя на главную страницу
        else:
            if user1:
                return HttpResponse('Ваша учетная запись заблокирована!')
            else:
                return HttpResponse('Неправильное имя или пароль')
    else:
        return render(request, 'login.html')  # выдаем пустую форму для входа


def register(request):
    if request.method == 'POST':
        data = request.POST
        user = User(email=data['email'], first_name=data['first_name'], last_name=data['last_name'],
                    birthday=data['birthday'], description=data['description'],
                    avatar=data['avatar'])  # объекты класса model.User, кроме пароля
        user.set_password(data['password'])  # пароль сразу преобразуется в хэш
        user.save()  # сохранение записи пользователя
        dj_login(request, user)  # вход пользователя
        return redirect('index')
    else:
        return render(request, 'register.html')  # на запрос GET возвращаем пустую форму для регистрации
    # return HttpResponse('Страница для <b>регистрации</b> пользователя на сайте')


def logout(request):
    dj_logout(request)
    return redirect('login')
    # return HttpResponse('Это представление выполняет <b>выход</b> и редирект на страницу входа')


def change_password(request):
    return HttpResponse('Обработчик изменения <b>пароля</b> пользователя')


def reset_password(request):
    return HttpResponse('Обработчик сброса <b>пароля</b> пользователя')
