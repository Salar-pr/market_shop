# Generated by Django 5.1.3 on 2024-12-03 16:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_alter_banner_options_alter_color_options_and_more'),
        ('product_order', '0002_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
    ]
