# Generated by Django 2.2.23 on 2021-05-14 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0011_activity_skills'),
    ]

    operations = [
        migrations.CreateModel(
            name='Presense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField(verbose_name='Первый день')),
                ('date_to', models.DateField(verbose_name='Последний день')),
                ('is_availabile', models.BooleanField(default=True, verbose_name='Является ли доступным')),
                ('specialist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.Specialist', verbose_name='Специалист')),
            ],
            options={
                'verbose_name': 'Присутствие',
                'verbose_name_plural': 'Присутствия',
                'db_table': 'presense',
                'ordering': ['date_from'],
            },
        ),
    ]
