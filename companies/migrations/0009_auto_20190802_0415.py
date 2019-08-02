# Generated by Django 2.2.3 on 2019-08-02 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0008_auto_20190712_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='size',
            field=models.CharField(choices=[('L', 'Large'), ('M', 'Medium'), ('S', 'Small'), ('U', 'Unknown')], max_length=1),
        ),
    ]
