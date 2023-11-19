from django.contrib.auth.models import Group
from django.core.mail import EmailMessage  # еще один вариант отправки писем
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone


account_access = Signal()  # вход в LMS

def send_login_user_email(**kwargs):
    template_name = 'registration/account_access_email.html'
    request = kwargs['request']
    context = {
        'request': request,
        'message': f"{timezone.now().isoformat()} кто-то вошел "
                   f"\n с учетной записью {request.POST['username']}"  # \n = перевод строки
    }
    email = EmailMessage(subject='Вход в аккаунт | Платформа жд.ст.Безымянка',
                         body=render_to_string(template_name, context),
                         to=[request.POST['username']] )
    email.content_subtype = 'html'  # можно форматировать?
    #email.send(fail_silently=False)  # отладка
    email.send(fail_silently=True)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def grant_pupil_rights(sender, instance, created=True, **kwargs):
    if created:  # сразу после создания НОВОГО (created=True) юзера автоматом добавим его в группу "Ученики"
        pupil = Group.objects.filter(name='Ученики')
        instance.groups.set(pupil)
        # print(f'Пользователь {instance} добавлен в группу "Ученики"')


account_access.connect(send_login_user_email)