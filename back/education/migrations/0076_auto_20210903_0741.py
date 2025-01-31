# Generated by Django 2.2.23 on 2021-09-03 07:41

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0075_auto_20210825_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Meta'),
        ),
        migrations.AlterField(
            model_name='skill_report',
            name='coefficient',
            field=models.FloatField(default=1, verbose_name='Коэффициент навыка на момент отчета'),
        ),
    ]
