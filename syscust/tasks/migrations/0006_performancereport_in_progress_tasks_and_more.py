# Generated by Django 5.0.7 on 2024-08-16 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_performancereport_points_alter_category_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='performancereport',
            name='in_progress_tasks',
            field=models.IntegerField(default=0, verbose_name='المهام قيد التنفيذ'),
        ),
        migrations.AddField(
            model_name='performancereport',
            name='total_tasks',
            field=models.IntegerField(default=0, verbose_name='المهام الكليّة'),
        ),
    ]
