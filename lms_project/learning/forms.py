from .models import Course, Review, Lesson
from django import forms
from django.forms.widgets import Textarea
from django.forms.utils import ValidationError


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course  # по какой модели работать
        fields = ('title', 'description', 'start_date', 'duration', 'count_lessons', 'price')
        # список и порядок полей в форме или '__all__'
        # хочется еще:
        # 1) подсказки как заполнители и формат поля для даты
        # 2) несколько полей в одной строке


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('content', )


class LessonForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label='Курс', empty_label='Выберите курс',
                                    required=True, help_text='Укажите курс, к которому добавляете урок')
    # при переопределении поля все атрибуты надо указать явно.
    # А по-хорошему это поле вообще надо скрыть и заполнить автоматом.
    preview = forms.CharField(widget=Textarea(attrs={'placeholder': 'Описание содержания урока',
                              'rows': 20, 'cols': 35}),
                              label='')
    # выделили на экране 700 символов, а в модели 200, но тут мы переопределили, а в БД поле текстовое
    # поэтому сохранение 700 символов будет работать, если не ограничим специально (см. clean_preview)
    error_css_class = 'error_field'  # HTML class для полей, не прошедших валидацию, в SCC прописал, но не работает.
    required_css_class = 'required_field'  # HTML class для обязательных полей

    class Meta:
        model = Lesson
        fields = ('name', 'preview', 'course')  # '__all__'
        # тут можно задать атрибуты для всех полей:
        # labels = {'name': '', 'preview': '', 'course': ''}
        # help_texts = {'name': 'Название урока', 'preview': 'Содержание урока'}
        # и т.п. но все равно рутины много и ненаглядно

    def clean_preview(self):  # переопределение метода проверки для одного поля
        preview_data = self.cleaned_data['preview']
        # извлекаем текст из проверенных данных формы (там 700 символов допустимы)
        if len(preview_data) > 200:
            raise ValidationError('Описание курса не должно быть длиннее 200 символов')
        return preview_data



