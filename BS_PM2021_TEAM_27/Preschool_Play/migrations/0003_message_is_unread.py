# Generated by Django 3.2 on 2021-04-14 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Preschool_Play', '0002_alter_child_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_unread',
            field=models.BooleanField(default=True),
        ),
    ]