# Generated by Django 2.2.23 on 2021-05-17 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0025_auto_20210517_0914'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='skill_report',
            unique_together={('job', 'skill')},
        ),
    ]
