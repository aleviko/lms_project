from django.contrib.auth.views import LoginView, LogoutView
# Наборчик для работы со сбросом пароля
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path
from .views import *

# список маршрутов. имя фиксированное
# (шаблон пути, контроллер или вложенный список маршрутов)
# представления для этих путей см. во views.py

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('change_password/', change_password, name='change_password'),
    # Обработчики сброса пароля - все настройки оставили по умолчанию, в т.ч. имена маршрутов (а почему тогда их вообще надо указывать?)
    # а шаблоны страниц сброса пароля переопределим на свои
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uuid64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
