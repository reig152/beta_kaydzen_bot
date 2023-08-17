# Generated by Django 4.2.4 on 2023-08-15 12:37

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("companies", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomPermission",
            fields=[],
            options={
                "verbose_name": "Право",
                "verbose_name_plural": "Права",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("auth.permission",),
            managers=[
                ("objects", django.contrib.auth.models.PermissionManager()),
            ],
        ),
        migrations.CreateModel(
            name="Role",
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
                ("name", models.CharField(max_length=100, unique=True)),
                (
                    "permissions",
                    models.ManyToManyField(blank=True, to="users.custompermission"),
                ),
            ],
            options={
                "verbose_name": "Роль",
                "verbose_name_plural": "Роли",
            },
        ),
        migrations.CreateModel(
            name="CustomUser",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "first_name",
                    models.CharField(blank=True, max_length=150, verbose_name="Имя"),
                ),
                (
                    "last_name",
                    models.CharField(blank=True, max_length=150, verbose_name="Фамилия"),
                ),
                (
                    "middle_name",
                    models.CharField(blank=True, max_length=150, verbose_name="Отчество"),
                ),
                (
                    "email",
                    models.EmailField(blank=True, max_length=254, verbose_name="Email"),
                ),
                (
                    "mobile",
                    models.CharField(blank=True, max_length=150, verbose_name="Телефон"),
                ),
                (
                    "telegram_username",
                    models.CharField(
                        blank=True,
                        max_length=40,
                        null=True,
                        unique=True,
                        verbose_name="Telegram username",
                    ),
                ),
                (
                    "position",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="Должность пользователя"
                    ),
                ),
                (
                    "company_name",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="companies.company",
                        verbose_name="Компания пользователя",
                    ),
                ),
                (
                    "custom_user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        related_name="custom_users",
                        to="users.custompermission",
                    ),
                ),
                (
                    "department_name",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="companies.department",
                        verbose_name="Департамент пользователя",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "role",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="users",
                        to="users.role",
                        verbose_name="Роль",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
