# Generated by Django 2.1.5 on 2022-11-14 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20221002_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagedata',
            name='photo',
            field=models.ImageField(upload_to='photos/'),
        ),
    ]
