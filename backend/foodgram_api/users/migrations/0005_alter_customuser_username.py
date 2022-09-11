# Generated by Django 4.1 on 2022-09-07 09:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_customuser_managers_and_more"),
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
                        message="Недопустимое значение поля.", regex="^[\\w.@+-]{3,15}$"
                    )
                ],
                verbose_name="Логин",
            ),
        ),
    ]
