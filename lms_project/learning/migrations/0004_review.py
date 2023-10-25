# Generated by Django 4.0 on 2023-10-24 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0002_alter_user_avatar'),
        ('learning', '0003_alter_course_options_alter_lesson_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=250, unique_for_year='sent_date', verbose_name='Текст отзыва')),
                ('sent_date', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning.course', verbose_name='Курс')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_app.user', verbose_name='Ученик')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ('-sent_date',),
                'unique_together': {('user', 'course')},
            },
        ),
    ]
