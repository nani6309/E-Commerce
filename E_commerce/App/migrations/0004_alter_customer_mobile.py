# Generated by Django 5.0.2 on 2024-05-27 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_rename_password_customer_locality_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='mobile',
            field=models.BigIntegerField(default=0),
        ),
    ]
