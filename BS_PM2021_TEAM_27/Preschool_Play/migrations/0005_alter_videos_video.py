# Generated by Django 3.2.2 on 2021-05-09 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Preschool_Play', '0004_alter_videos_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videos',
            name='video',
            field=models.FileField(upload_to='uploads/'),
        ),
    ]
