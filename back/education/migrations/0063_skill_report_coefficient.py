# Generated by Django 2.2.23 on 2021-08-12 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0062_auto_20210811_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill_report',
            name='coefficient',
            field=models.FloatField(default=0, verbose_name='Коэффициент навыка на момент отчета'),
        ),
    ]
