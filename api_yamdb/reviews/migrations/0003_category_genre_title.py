# Generated by Django 3.2.13 on 2022-06-09 11:46

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220608_0205'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите имя категории', max_length=256, verbose_name='Имя категории')),
                ('slug', models.SlugField(help_text='Введите короткий тэг категории', unique=True, verbose_name='Тэг категории')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите имя жанра', max_length=40, verbose_name='Имя жанра')),
                ('slug', models.SlugField(help_text='Введите короткий тэг жанра', max_length=20, unique=True, verbose_name='Тэг жанра')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите имя произведения', max_length=20, verbose_name='Имя произведения')),
                ('year', models.IntegerField(help_text='Введите год создания произведения, yyyy', validators=[django.core.validators.MaxValueValidator(2022)], verbose_name='Дата создания')),
                ('description', models.TextField(blank=True, default='', help_text='Подрбности/описание', null=True, verbose_name='Подробности')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='title', to='reviews.category', verbose_name='Категория произведения')),
                ('genre', models.ManyToManyField(blank=True, related_name='title', to='reviews.Genre', verbose_name='Жанры произведения')),
            ],
        ),
    ]
