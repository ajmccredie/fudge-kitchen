# Generated by Django 4.2.9 on 2024-06-05 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_alter_subscriptionproduct_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionproduct',
            name='description',
            field=models.TextField(default='Product Description', max_length=600),
        ),
        migrations.AlterField(
            model_name='subscriptionproduct',
            name='image',
            field=models.ImageField(default='static/images/default_text_logo.png', upload_to=''),
        ),
        migrations.AlterField(
            model_name='subscriptionproduct',
            name='name',
            field=models.CharField(default='Product Name', max_length=254),
        ),
    ]
