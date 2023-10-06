from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.http import HttpResponse

# Create your views here.
# request содержит объект текущего запроса, указывать обязательно, несмотря на предупреждения


def login(request):
    if request.method == 'POST':
        # получаем данные из полей формы логина и получаем запись из модели user для входящего пользователя
        data = request.POST
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:  # пользователь найден (non none) и не заблокирован
            login(request, user)  # вход
            return redirect('index')  # перенаправляем пользователя на главную страницу
        else:
            if user:
                return HttpResponse('Ваша учетная запись заблокирована!')
            else:
                return HttpResponse('Неправильное имя или пароль')

    else:
        return render(request, 'login.html')  # выдаем пустую форму для входа



def register(request):
    return HttpResponse('Страница для <b>регистрации</b> пользователя на сайте')


def logout(request):
    return HttpResponse('Это представление выполняет <b>выход</b> и редирект на страницу входа')


def change_password(request):
    return HttpResponse('Обработчик изменения <b>пароля</b> пользователя')


def reset_password(request):
    return HttpResponse('Обработчик сброса <b>пароля</b> пользователя')
