# Generated by Django 2.2.23 on 2021-06-09 06:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0042_auto_20210608_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='method',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='education.Method', verbose_name='Способ'),
        ),
    ]
