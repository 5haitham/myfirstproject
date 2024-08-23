# Generated by Django 5.0.7 on 2024-08-09 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='completed',
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('Not Started', 'لم يُنفذ'), ('In Progress', 'قيد التنفيذ'), ('Completed', 'منفذ')], default='Not Started', max_length=20),
        ),
    ]
