# Generated by Django 3.2.2 on 2021-05-09 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Preschool_Play', '0002_videos'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='videos',
            options={'verbose_name': 'uploads', 'verbose_name_plural': 'uploads'},
        ),
        migrations.AlterField(
            model_name='videos',
            name='video',
            field=models.FileField(upload_to='uploads/'),
        ),
    ]