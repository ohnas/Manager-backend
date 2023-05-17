# Generated by Django 4.1.4 on 2023-05-17 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("brands", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=200, unique=True)),
                ("price", models.PositiveIntegerField(default=0)),
                ("cost", models.PositiveIntegerField(default=0)),
                ("delivery_price", models.PositiveIntegerField(default=0)),
                ("logistic_fee", models.PositiveIntegerField(default=0)),
                ("quantity", models.PositiveIntegerField(default=0)),
                (
                    "gift_quantity",
                    models.PositiveIntegerField(blank=True, default=0, null=True),
                ),
                (
                    "brand",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="brands.brand"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Options",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=200, unique=True)),
                ("price", models.PositiveIntegerField()),
                ("logistic_fee", models.PositiveIntegerField()),
                ("quantity", models.PositiveIntegerField()),
                (
                    "gift_quantity",
                    models.PositiveIntegerField(blank=True, default=0, null=True),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
