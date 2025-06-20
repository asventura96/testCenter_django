# Generated by Django 5.2.1 on 2025-06-05 19:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("certifications", "0002_rename_durantion_certification_duration"),
        ("clients", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TestCenter",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("notes", models.TextField(blank=True, null=True)),
                ("idle", models.BooleanField(default=False)),
            ],
            options={
                "db_table": "tb_test_center",
            },
        ),
        migrations.CreateModel(
            name="TestCenterExam",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("date", models.DateTimeField()),
                ("presence", models.BooleanField(default=False)),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "certification",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="certifications.certification",
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="clients.client"
                    ),
                ),
                (
                    "testCenter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="testCenter.testcenter",
                    ),
                ),
            ],
            options={
                "db_table": "tb_testCenter-exam",
            },
        ),
    ]
