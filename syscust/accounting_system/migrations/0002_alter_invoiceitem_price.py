# Generated by Django 5.0.7 on 2024-07-29 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceitem',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]