# Generated by Django 3.2.9 on 2021-11-13 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hw_session', '0008_alter_session_data_break_interval'),
    ]

    operations = [
        migrations.AddField(
            model_name='session_data',
            name='goal_accomplished',
            field=models.BooleanField(null=True),
        ),
    ]
