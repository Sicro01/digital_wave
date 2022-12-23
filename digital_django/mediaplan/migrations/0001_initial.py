# Generated by Django 4.1.2 on 2022-12-10 16:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Ad",
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
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Channel",
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
                ("code", models.CharField(max_length=5, unique=True)),
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Country",
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
                ("code", models.CharField(max_length=5, unique=True)),
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Device",
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
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Phase",
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
                ("name", models.CharField(max_length=100)),
                (
                    "description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("start_date", models.DateField(default=datetime.date.today)),
                ("end_date", models.DateField(default=datetime.date.today)),
                ("slug", models.SlugField(blank=True, max_length=100, null=True)),
                (
                    "budget",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "budget_allocated",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("auto_allocate", models.BooleanField(default=False)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ("-date_added",),
            },
        ),
        migrations.CreateModel(
            name="Plan",
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
                ("name", models.CharField(max_length=100)),
                (
                    "description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("slug", models.SlugField(blank=True, max_length=100, null=True)),
                (
                    "budget",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "budget_allocated",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("auto_allocate", models.BooleanField(default=False)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ("-date_modified",),
            },
        ),
        migrations.CreateModel(
            name="Strategy",
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
                ("name", models.CharField(max_length=100)),
                (
                    "description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("start_date", models.DateField(default=datetime.date.today)),
                ("end_date", models.DateField(default=datetime.date.today)),
                ("slug", models.SlugField(blank=True, max_length=100, null=True)),
                (
                    "budget",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "budget_allocated",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("auto_allocate", models.BooleanField(default=False)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                (
                    "phase",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="strategies",
                        to="mediaplan.phase",
                    ),
                ),
            ],
            options={
                "ordering": ("-date_added",),
            },
        ),
        migrations.CreateModel(
            name="TargetChannel",
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
                ("code", models.CharField(default=1, max_length=5)),
                ("name", models.CharField(default="", max_length=100)),
                (
                    "budget",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "budget_allocated",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("auto_allocate", models.BooleanField(default=False)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                (
                    "channel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mediaplan.channel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TargetDevice",
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
                (
                    "budget",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "budget_allocated",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("auto_allocate", models.BooleanField(default=False)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                (
                    "device",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mediaplan.device",
                    ),
                ),
                (
                    "target_channel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mediaplan.targetchannel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TargetCountry",
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
                ("code", models.CharField(default=1, max_length=5)),
                ("name", models.CharField(default="", max_length=100)),
                (
                    "budget",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "budget_allocated",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("auto_allocate", models.BooleanField(default=False)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mediaplan.country",
                    ),
                ),
                (
                    "strategy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mediaplan.strategy",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="targetchannel",
            name="target_country",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="mediaplan.targetcountry",
            ),
        ),
        migrations.CreateModel(
            name="TargetAd",
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
                (
                    "budget",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "budget_allocated",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("auto_allocate", models.BooleanField(default=False)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                (
                    "ad",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="mediaplan.ad"
                    ),
                ),
                (
                    "target_device",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mediaplan.targetdevice",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="phase",
            name="plan",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="phases",
                to="mediaplan.plan",
            ),
        ),
        migrations.AddField(
            model_name="device",
            name="target_channels",
            field=models.ManyToManyField(
                blank=True,
                through="mediaplan.TargetDevice",
                to="mediaplan.targetchannel",
            ),
        ),
        migrations.CreateModel(
            name="Creative",
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
                ("name", models.CharField(max_length=100)),
                (
                    "budget",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "budget_allocated",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                (
                    "target_ad",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="creatives",
                        to="mediaplan.targetad",
                    ),
                ),
            ],
            options={
                "ordering": ("name",),
            },
        ),
        migrations.AddField(
            model_name="country",
            name="strategies",
            field=models.ManyToManyField(
                blank=True, through="mediaplan.TargetCountry", to="mediaplan.strategy"
            ),
        ),
        migrations.AddField(
            model_name="channel",
            name="target_countries",
            field=models.ManyToManyField(
                blank=True,
                through="mediaplan.TargetChannel",
                to="mediaplan.targetcountry",
            ),
        ),
        migrations.AddField(
            model_name="ad",
            name="target_devices",
            field=models.ManyToManyField(
                blank=True, through="mediaplan.TargetAd", to="mediaplan.targetdevice"
            ),
        ),
    ]
