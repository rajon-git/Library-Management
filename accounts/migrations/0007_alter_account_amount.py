# Generated by Django 5.1 on 2024-08-26 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_rename_date_joined_account_date_join_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='amount',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
