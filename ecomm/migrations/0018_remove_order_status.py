# Generated by Django 3.2 on 2024-07-16 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0017_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
    ]
