# Generated by Django 2.2.23 on 2021-05-14 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0014_option'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.TextField(max_length=200, unique=True, verbose_name='Название'),
        ),
    ]
