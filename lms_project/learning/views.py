from django.http import HttpResponse
from django.shortcuts import render


# request содержит объект текущего запроса, указывать обязательно, несмотря на предупреждения
def login(request):
    return HttpResponse('Страница для входа пользователя на сайт')


def register(request):
    return HttpResponse('Страница для регистрации пользователя на сайте')


def logout(request):
    return HttpResponse('Это представление выполняет выход и редирект на страницу входа')


def change_password(request):
    return HttpResponse('Обработчик изменения пароля пользователя')


def reset_password(request):
    return HttpResponse('Обработчик сброса паорля пользователя')
