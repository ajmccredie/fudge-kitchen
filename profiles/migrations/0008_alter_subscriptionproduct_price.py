# Generated by Django 4.2.9 on 2024-06-05 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_alter_subscriptionproduct_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionproduct',
            name='price',
            field=models.DecimalField(decimal_places=2, default=7.0, max_digits=6, null=True),
        ),
    ]
