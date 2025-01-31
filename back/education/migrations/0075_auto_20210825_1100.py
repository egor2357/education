# Generated by Django 2.2.23 on 2021-08-25 11:00

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0074_notification'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='announcement',
            options={'ordering': ['-creation_date'], 'verbose_name': 'Обращение руководства', 'verbose_name_plural': 'Обращения руководства'},
        ),
        migrations.AddField(
            model_name='notification',
            name='meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True, verbose_name='Meta'),
        ),
    ]
