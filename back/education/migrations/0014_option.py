# Generated by Django 2.2.23 on 2021-05-14 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0013_auto_20210514_0844'),
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.TextField(max_length=200, verbose_name='Подпись')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.Activity', verbose_name='Вид деятельсности')),
                ('method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='education.Method', verbose_name='Способ проведения занятия')),
                ('specialist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.Specialist', verbose_name='Специалист')),
            ],
            options={
                'verbose_name': 'Вариант занятия',
                'verbose_name_plural': 'Варианты занятия',
                'db_table': 'option',
                'ordering': ['specialist'],
            },
        ),
    ]
