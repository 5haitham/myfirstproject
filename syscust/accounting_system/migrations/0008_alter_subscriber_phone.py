# Generated by Django 5.0.7 on 2024-07-30 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_system', '0007_alter_subscriber_address_alter_subscriber_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
