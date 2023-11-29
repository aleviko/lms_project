from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase, Client
from django.utils import timezone

# Create your tests here.


class AuthAppTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.student_group = Group.objects.create(name='Ученики')  # группу придется создать.
        # кстати, раз она у нас "предопределенная", то и в продакшне надо бы создавать
        cls.student_perms = Permission.objects.filter(content_type__app_label='learning',
                                                      codename__in=['view', 'add_tracking'])
        cls.student_group.permissions.set(cls.student_perms)  # выдача прав

    def setUp(self) -> None:

        # тест на неправильный ввод - пароли не совпадают
        self.user_invalid_register_data = {
            'username': 'student',
            'email': 'student@example.com',
            'birthday': '01.01.2023', # timezone.now().date(),
            'password1': 'student1234',
            'password2': 'student4321'
        }

        # тест на правильный ввод
        self.user_valid_register_data = {
            'username': 'student',
            'email': 'student@example.com',
            'birthday': '01.01.2023', # timezone.now().date(),
            'password1': 'student1234',
            'password2': 'student1234'
        }

        self.user_login_data_with_rememdber = {  # тест на галочку "запомнить"
            'username': 'student@example.com',
            'password1': 'student1234',
            'is_remember': 'on'
        }

        self.user_login_data_without_rememdber = {  # тест на галочку "запомнить"
            'username': 'student@example.com',
            'password1': 'student1234',
            'is_remember': 'off'
        }

        self.invalid_login_data = {  # тест на неправильный пароль
            'username': 'student@example.com',
            'password1': 'admin1234'
        }

        self.admin = get_user_model().objects.create_superuser(  # админ
            username='admin',
            email='admin@example.com',
            password='admin1234'
        )

        self.client = Client()  # имитатор браузера
        self.register = reverse('register')
        self.login = reverse('login')
        self.logout = reverse('logout')
        self.index = reverse('index')


    def test_get_register_view(self):  # префикс test_ обязателен
        response = self.client.get(path=self.register)
        self.assertEqual(response.status_code, 200)  # успешно?
        self.assertTemplateUsed(response, 'register.html')  # тем ли шаблоном выдан результат


    def test_post_register_view(self):  # имитация POST запроса с коррекными данными
        response = self.client.post(path=self.register, data=self.user_valid_register_data)
        self.assertEqual(response.status_code, 200)  # успешно?