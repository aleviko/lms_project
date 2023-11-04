from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def grant_pupil_rights(sender, instance, created=True, **kwargs):
    if created:  # сразу после создания НОВОГО (created=True) юзера автоматом добавим его в группу "Ученики"
        pupil = Group.objects.filter(name='Ученики')
        instance.groups.set(pupil)
        print(f'Пользователь {instance} добавлен в группу "Ученики"')
