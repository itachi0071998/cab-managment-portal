# Generated by Django 5.0.3 on 2024-03-13 10:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0003_alter_cab_state"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookings",
            name="start_time",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]