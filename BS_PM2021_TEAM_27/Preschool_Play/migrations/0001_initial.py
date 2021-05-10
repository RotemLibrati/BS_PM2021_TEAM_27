# Generated by Django 3.2.2 on 2021-05-09 11:57

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('suspension_time', models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0))),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('path', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('music', 'music'), ('picture', 'picture')], default='picture', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(default='', max_length=100)),
                ('age', models.IntegerField(default=0)),
                ('points', models.IntegerField(default=0)),
                ('type', models.CharField(choices=[('parent', 'parent'), ('teacher', 'teacher')], default='parent', max_length=10)),
                ('is_admin', models.BooleanField(default=False)),
                ('suspension_time', models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0))),
                ('total_minutes', models.FloatField(default=0)),
                ('last_login', models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0))),
                ('rank', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=1)),
                ('limit', models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0))),
                ('auth', models.BooleanField(default=False)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.CharField(blank=True, max_length=50)),
                ('amount', models.IntegerField(default=0)),
                ('comment', models.CharField(blank=True, max_length=250, null=True)),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('child', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='score', to='Preschool_Play.child')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=256)),
                ('seen', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=50)),
                ('body', models.CharField(blank=True, max_length=250)),
                ('sent_date', models.DateTimeField(auto_now_add=True)),
                ('deleted_by_sender', models.BooleanField(default=False)),
                ('deleted_by_receiver', models.BooleanField(default=False)),
                ('is_public', models.BooleanField(default=False)),
                ('is_unread', models.BooleanField(default=True)),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Kindergarten',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50)),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teacher', to='Preschool_Play.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='child',
            name='kindergarten',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Preschool_Play.kindergarten'),
        ),
        migrations.AddField(
            model_name='child',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child', to='Preschool_Play.userprofile'),
        ),
        migrations.AddField(
            model_name='child',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student', to='Preschool_Play.userprofile'),
        ),
    ]
