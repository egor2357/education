# Generated by Django 2.2.23 on 2021-06-22 09:12

from django.db import migrations, models
import education.models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0049_auto_20210622_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_file',
            name='file',
            field=models.FileField(max_length=255, upload_to=education.models.Job_file.get_file_upload_to, verbose_name='Файл'),
        ),
        migrations.AlterField(
            model_name='option_file',
            name='file',
            field=models.FileField(max_length=255, upload_to=education.models.Option_file.get_file_upload_to, verbose_name='Файл'),
        ),
    ]
