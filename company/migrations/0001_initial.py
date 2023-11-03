# Generated by Django 4.2.5 on 2023-11-03 12:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("common", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Company",
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
                ("created_at", models.DateField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("is_visible", models.BooleanField(default=True)),
                (
                    "invitations",
                    models.ManyToManyField(
                        blank=True,
                        related_name="company_invitations",
                        to="common.invitation",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Companies",
            },
        ),
    ]
