from django.urls import path
from .views import *

# список маршрутов. имя фиксированное
# (шаблон пути, контроллер или вложенный список маршрутов)
# представления для этих путей см. во views.py

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('change_password/', change_password, name='change_password'),
    path('reset_password/', reset_password, name='reset_password'),
]
