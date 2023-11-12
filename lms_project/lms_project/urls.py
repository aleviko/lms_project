"""lms_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # для доступа к значениям настроек из кода !в доках мелькает про повышение уязвимости сайта при этом - поизучать!
from django.conf.urls.static import static  # создает маршрут к файлам !только в тестовом режиме сервера!


# ссылки на обработчики ошибок. формат: handler<код ошибки>
handler500 = 'lms_project.views.server_error'
handler404 = 'lms_project.views.page_not_found'
handler403 = 'lms_project.views.forbidden'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_app.urls')),  # подключить вложенный список маршрутов из auth_app
    path('courses/', include('learning.urls')),
    path('__debug__', include('debug_toolbar.urls')),  # для отладки
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
