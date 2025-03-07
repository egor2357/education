# Generated by Django 2.2.23 on 2025-01-21 07:55

import django.contrib.postgres.fields.ranges
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0087_auto_20250121_0724'),
    ]

    operations = [
        migrations.AddField(
            model_name='development_direction',
            name='lifetime',
            field=django.contrib.postgres.fields.ranges.DateRangeField(default=('2020-01-01', None), verbose_name='Время жизни'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='educational_area',
            name='lifetime',
            field=django.contrib.postgres.fields.ranges.DateRangeField(default=('2020-01-01', None), verbose_name='Время жизни'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exercise',
            name='lifetime',
            field=django.contrib.postgres.fields.ranges.DateRangeField(default=('2020-01-01', None), verbose_name='Время жизни'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result',
            name='lifetime',
            field=django.contrib.postgres.fields.ranges.DateRangeField(default=('2020-01-01', None), verbose_name='Время жизни'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skill',
            name='lifetime',
            field=django.contrib.postgres.fields.ranges.DateRangeField(default=('2020-01-01', None), verbose_name='Время жизни'),
            preserve_default=False,
        ),
    ]
