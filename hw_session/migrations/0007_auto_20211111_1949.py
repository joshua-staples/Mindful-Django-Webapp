# Generated by Django 3.2.9 on 2021-11-12 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hw_session', '0006_remove_hw_data_hw_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='session_data',
            name='break_interval',
            field=models.CharField(choices=[(0.25, '15mins'), (0.5, '30mins'), (0.75, '45mins'), (1, '1hr'), (1.25, '1hr 15mins'), (1.5, '1hr 30mins')], default=1.25, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='session_data',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
