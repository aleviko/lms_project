# from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# request содержит объект текущего запроса, указывать обязательно, несмотря на предупреждения


def login(request):
    return HttpResponse('Страница для <b>вход</b>а пользователя на сайт')


def register(request):
    return HttpResponse('Страница для <b>регистрации</b> пользователя на сайте')


def logout(request):
    return HttpResponse('Это представление выполняет <b>выход</b> и редирект на страницу входа')


def change_password(request):
    return HttpResponse('Обработчик изменения <b>пароля</b> пользователя')


def reset_password(request):
    return HttpResponse('Обработчик сброса <b>пароля</b> пользователя')
