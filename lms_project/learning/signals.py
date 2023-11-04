from django.db.models.signals import pre_save
from django.dispatch import Signal
from .models import Course, Lesson


set_views = Signal()  # самодельный сигнал для подсчета посещений

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

# подключение сигналов
pre_save.connect(check_lessons_qty, sender=Lesson)
set_views.connect(incr_views)

#'views'
#{'1': 2, '11': 1, '12': 2, '13': 1, '15': 1, '18': 2, '19': 1, '2': 4}
#{'1': 3, '11': 1, '12': 3, '13': 1, '15': 1, '18': 2, '19': 1, '2': 4}
#{'1': 3, '11': 1, '12': 3, '13': 1, '15': 1, '18': 7, '19': 1, '2': 4}