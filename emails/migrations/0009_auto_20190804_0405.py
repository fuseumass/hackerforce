# Generated by Django 2.2.3 on 2019-08-04 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0008_email_sent_contacts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='time_scheduled',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='time_sent',
            field=models.DateTimeField(blank=True),
        ),
    ]
