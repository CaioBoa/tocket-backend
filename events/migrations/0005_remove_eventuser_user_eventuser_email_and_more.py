# Generated by Django 4.2.1 on 2023-05-31 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_rename_usuario_eventuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventuser',
            name='user',
        ),
        migrations.AddField(
            model_name='eventuser',
            name='email',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='eventuser',
            name='password',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='eventuser',
            name='username',
            field=models.CharField(default='', max_length=200),
        ),
    ]
