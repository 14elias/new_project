# Generated by Django 5.1.5 on 2025-02-04 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_cartitem_cart_alter_cartitem_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='title',
        ),
    ]
