# Generated by Django 5.0.6 on 2024-06-26 00:09

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("vege", "0003_user"),
    ]

    operations = [
        migrations.DeleteModel(
            name="User",
        ),
    ]