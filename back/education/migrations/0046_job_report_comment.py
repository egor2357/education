# Generated by Django 2.2.23 on 2021-06-15 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0045_remove_skill_report_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='report_comment',
            field=models.TextField(blank=True, verbose_name='Комментарий по результатам занятия'),
        ),
    ]
