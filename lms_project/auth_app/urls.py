from django.contrib.auth.views import LoginView, LogoutView
# Наборчик для работы со сбросом и сменой пароля
from django.contrib.auth.views import (PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
    PasswordChangeView, PasswordChangeDoneView)


from django.urls import path
from .views import *

# список маршрутов. имя фиксированное
# (шаблон пути, контроллер или вложенный список маршрутов)
# представления для этих путей см. во views.py

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    # смена пароля
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),  # предопределенное имя шаблона: password_change_form
    path('password-change/done', PasswordChangeDoneView.as_view(), name='password_change_done'),  # предопределенное имя шаблона: password_change_done
    # Обработчики сброса пароля - все настройки оставили по умолчанию, в т.ч. имена маршрутов (а почему тогда их вообще надо указывать?)
    # а шаблоны страниц сброса пароля переопределим на свои
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
