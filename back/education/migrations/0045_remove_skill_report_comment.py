# Generated by Django 2.2.23 on 2021-06-15 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0044_auto_20210609_1210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skill_report',
            name='comment',
        ),
    ]
