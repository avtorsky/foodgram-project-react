# Generated by Django 4.1 on 2022-09-07 13:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_alter_customuser_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="username",
            field=models.CharField(
                max_length=150,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Недопустимое значение поля.",
                        regex="^[\\w.@+-]{3,150}$",
                    )
                ],
                verbose_name="Логин",
            ),
        ),
    ]
