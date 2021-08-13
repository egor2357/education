# Generated by Django 2.2.23 on 2021-08-13 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0064_auto_20210812_1255'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата-время создания')),
                ('caption', models.TextField(verbose_name='Краткое описание')),
                ('text', models.TextField(verbose_name='Текст обращения')),
            ],
            options={
                'verbose_name': 'Обращение руководсва',
                'verbose_name_plural': 'Обращения руководсва',
                'db_table': 'announcement',
                'ordering': ['-creation_date'],
            },
        ),
        migrations.AlterField(
            model_name='mission',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата-время создания'),
        ),
    ]
