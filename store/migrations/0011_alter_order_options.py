# Generated by Django 5.1.5 on 2025-02-06 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_customer_birth_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'can cancel order')]},
        ),
    ]
