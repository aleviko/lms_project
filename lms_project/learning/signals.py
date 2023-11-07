from django.db.models.signals import pre_save
from django.dispatch import Signal
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from .models import Course, Lesson



set_views = Signal()  # самодельный сигнал для подсчета посещений
course_enroll = Signal()  # запись на курс
get_certificate = Signal()  # запрос документа

def check_lessons_qty(sender, instance, **kwargs):
    error = None
    lessons_qty = sender.objects.filter(course=instance.course).count()
    preset_count = Course.objects.filter(id=instance.course.id).values('count_lessons')[0]['count_lessons']

    if lessons_qty >= preset_count:
        error = f'В описании курса указано {preset_count} уроков и этот урок уже лишний. '\
                f'Очень удобно и приятно узнать об этом в самом конце?'\
                f'Особенно, когда вы - автор курса и вольны определять в нем все? ;)'
    return error

def incr_views(sender, **kwargs):  # подсчет посещений
    session = kwargs['session']
    views = session.setdefault('views', {})  # счетчик посещений страницы извлечение, если есть
    course_id = str(kwargs['id'])  # ключ страницы
    count = views.get(course_id, 0)  # извлечение хранимого счетчика (если есть или 0)
    views[course_id] = count + 1
    session['views'] = views
    session.modified = True


def send_enroll_email(**kwargs):
    template_name = 'emails/enroll_email.html'
    course = Course.objects.get(id=kwargs['course_id'])
    context = {
        'course': course,
        'message': f'Вы записались на курс {course.title}. '
                   f'Курс состоит из {course.count_lessons} уроков '
                   f'(но это не точно, т.к. наша LMS странная ;)) '
                   f'Начало занятий {course.start_date}'
        # теги здесь не работают, а жаль. в итоге пишу все буквы в шаблоне, а этот текст не использую
    }
    send_mail(subject=f'Вы записались на курс {course.title}.| Платформа жд.ст.Безымянка!',
              message='',  # для plain text?
              from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=[kwargs['request'].user.email],
              html_message=render_to_string(template_name, context, kwargs['request']),  # генерация хтмл по шаблону
              fail_silently=False  # валиться в ошибку при неотправке. если не спамим на непроверенные адреса, то так лучше
              )

def send_user_certificate(**kwargs):
    template_name = 'emails/certificate_email.html'
    context = {
        'message': 'Поздравляем с успешным окончанием курса!'
        '\nСертификат находится во вложении'
    }
    email = EmailMultiAlternatives(subject='Сертификат о прохождении курса | Платформа Безымянка',
                                   to=[kwargs['sender'].email])
    email.attach_alternative(render_to_string(template_name, context), mimetype='text/html')
    # print(settings.MEDIA_ROOT + '/certificates/certificate.png')  # у меня на / упорно ругается, заменил на +
    email.attach_file(path=settings.MEDIA_ROOT + '/certificates/certificate.png', mimetype='image/png') # path=абсолютный путь
    email.send(fail_silently=True)



# подключение сигналов
pre_save.connect(check_lessons_qty, sender=Lesson)
set_views.connect(incr_views)
course_enroll.connect(send_enroll_email)
get_certificate.connect(send_user_certificate)
#следы посещений страниц (в третий раз целенеправленно тыкал в один курс 5 раз
#'views'
#{'1': 2, '11': 1, '12': 2, '13': 1, '15': 1, '18': 2, '19': 1, '2': 4}
#{'1': 3, '11': 1, '12': 3, '13': 1, '15': 1, '18': 2, '19': 1, '2': 4}
#{'1': 3, '11': 1, '12': 3, '13': 1, '15': 1, '18': 7, '19': 1, '2': 4}