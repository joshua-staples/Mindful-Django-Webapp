# Generated by Django 3.2.8 on 2021-11-13 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hw_session', '0010_session_data_completed_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='hw_data',
            name='loadedAt',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]