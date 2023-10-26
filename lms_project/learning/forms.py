from .models import Course, Review
from django import forms


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ('title', 'description', 'start_date', 'duration', 'count_lessons', 'price')  # список и порядок полей в форме будет взят отсюда
        # хочется еще:
        # 1) подсказки как заполнители и формат поля для даты
        # 2) несколько полей в одной строке

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('content', )