# Generated by Django 2.2.3 on 2019-08-05 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0009_auto_20190804_0405'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='attach_packet',
            field=models.BooleanField(default=False, help_text='Whether the sponsorship packet should be attached'),
        ),
    ]
