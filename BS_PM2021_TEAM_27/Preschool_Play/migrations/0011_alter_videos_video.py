# Generated by Django 3.2.2 on 2021-05-09 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Preschool_Play', '0010_auto_20210509_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videos',
            name='video',
            field=models.FileField(upload_to='media/'),
        ),
    ]
