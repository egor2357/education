# Generated by Django 2.2.23 on 2021-05-14 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0015_auto_20210514_1223'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата проведения')),
                ('start_time', models.TimeField(verbose_name='Время начала')),
                ('comment', models.TextField(verbose_name='Комментарий по занятию')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.Option', verbose_name='Вариант занятия')),
            ],
            options={
                'verbose_name': 'Занятие',
                'verbose_name_plural': 'Занятия',
                'db_table': 'job',
                'ordering': ['date'],
            },
        ),
    ]
