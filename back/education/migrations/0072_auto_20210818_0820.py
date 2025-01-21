# Generated by Django 2.2.23 on 2021-08-18 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0071_auto_20210818_0800'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='talent',
            options={'ordering': ['-creation_date'], 'verbose_name': 'Талант', 'verbose_name_plural': 'Таланты'},
        ),
        migrations.AlterField(
            model_name='task_group',
            name='responsible',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responsible_task_groups', to='education.Specialist', verbose_name='Ответственный'),
        ),
    ]
