# Generated by Django 4.2.5 on 2023-11-06 20:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("company", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="company",
            name="invitations",
        ),
        migrations.RemoveField(
            model_name="company",
            name="user_requests",
        ),
    ]
