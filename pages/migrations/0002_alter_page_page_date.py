# Generated by Django 4.1.4 on 2023-03-07 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="page",
            name="page_date",
            field=models.DateField(unique=True),
        ),
    ]
