# Generated by Django 4.1.4 on 2023-01-02 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sites", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="site",
            name="api_key",
            field=models.CharField(default="", max_length=150),
        ),
        migrations.AddField(
            model_name="site",
            name="secret_key",
            field=models.CharField(default="", max_length=150),
        ),
    ]