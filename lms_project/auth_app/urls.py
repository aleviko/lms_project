from django.urls import path
from .views import *

# список маршрутов. имя фиксированное
# (шаблон пути, контроллер или вложенный список маршрутов)
urlpatterns = [
    path('login/', login),
    path('register/', register),
    path('logout/', logout),
    path('change_password/', change_password),
    path('reset_password/', reset_password),
]
