from django.contrib import admin
from .models import Course, Lesson, Review
# Register your models here.

# настройки вида моделей в АДМИНКЕ
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'price',
                    #'authors',  # поля many:many в таблицу не выводятся
                    'start_date', 'description', )  # список полей для вывода
    # в ТАБЛИЦЕ, без этого выводится только первое поле
    # Запятые в конце лучше вешать, т.к. иначе при одном поле пайтон считает это строкой и ругается
    exclude = ('price', )  # напротив, какие поля НЕ выводить
    # в ФОРМЕ!
    # Т.е. это настройки для разных страниц и работают они параллельно!
    search_fields = ('^title', 'start_date', 'description', )  # список полей, по которым разрешить поиск
    # search_fields = ('=title',)  # НЕ РАБОТАЕТ! поиск по точному совпадению (но без учета регистра)
    # search_fields = ('^title',)  # "начинается с..."
    # search_fields = ('@title',)  # "Полнотекстовый поиск, работает ТОЛЬКО с MySQL" - у меня ВАЛИТ СЕРВЕР
    # если перед именем поля поставить "=", поиск по нему будет по точному совпадению
    list_editable = ('start_date', 'price', )  # список полей ТАБЛИЦЫ, доступных для редактирования "in place"
    list_per_page = 2  # кол-во записей на страницу (но будет доступна кнопка "показать все")
    actions_on_top = False  # ВЫключает поле "Действие" НАД таблицей, у меня по умолчанию ВКЛЮЧЕНО
    actions_on_bottom = True  # Включает поле "Действие" ПОД таблицей, False - выключает
    actions_selection_counter = True  # Включить показ кол-ва выбранных записей
    save_on_top = True  # Добавить блок с кнопками управления записью ВВЕРХУ ФОРМЫ, внизу не отключаются
    list_display_links = ('title', 'description', )  # список полей, которые будут гиперссылками для
    # перехода в ФОРМУ записи. "edit in place" поля нельзя использовать
    filter_horizontal = ('authors', )  # выбор множества значений из списка в форме


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'name', 'preview', )
    list_display_links = ('course', 'name', 'preview', )
    search_fields = ('name', )
    actions_on_top = False
    actions_on_bottom = False
    list_per_page = 2
    actions_selection_counter = True
    # хочется добавить в форму кнопку "Отмена" или "Назад" и поправить названия имеющихся, но не вижу способа


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'sent_date')
    search_fields = ('content', )
    list_per_page = 100