# Generated by Django 4.1.4 on 2023-02-02 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_product_delivery_price_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="options",
            name="gift_quantity",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]