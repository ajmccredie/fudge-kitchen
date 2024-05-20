# Generated by Django 4.2.9 on 2024-05-20 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Allergen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('symbol', models.ImageField(blank=True, null=True, upload_to='allergens/')),
            ],
        ),
        migrations.CreateModel(
            name='EdibleProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plant_based', models.BooleanField(default=False)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('flavour', models.CharField(blank=True, max_length=254, null=True)),
                ('guest_flavour', models.BooleanField(default=False)),
                ('details', models.TextField()),
                ('ingredients', models.TextField()),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('weight', models.PositiveIntegerField(choices=[(100, '100g'), (400, '400g'), (800, '800g')], default=400, help_text='Weight in grams')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('rating', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('image_url', models.URLField(blank=True, max_length=1024, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('gluten', models.BooleanField(default=False, verbose_name='Gluten')),
                ('crustaceans', models.BooleanField(default=False, verbose_name='Crustaceans')),
                ('eggs', models.BooleanField(default=False, verbose_name='Eggs')),
                ('fish', models.BooleanField(default=False, verbose_name='Fish')),
                ('peanuts', models.BooleanField(default=False, verbose_name='Peanuts')),
                ('soybeans', models.BooleanField(default=False, verbose_name='Soybeans')),
                ('milk', models.BooleanField(default=False, verbose_name='Milk')),
                ('nuts', models.BooleanField(default=False, verbose_name='Nuts')),
                ('celery', models.BooleanField(default=False, verbose_name='Celery')),
                ('mustard', models.BooleanField(default=False, verbose_name='Mustard')),
                ('sesame_seeds', models.BooleanField(default=False, verbose_name='Sesame Seeds')),
                ('sulphur_dioxide_and_sulphites', models.BooleanField(default=False, verbose_name='Sulphur Dioxide and Sulphites')),
                ('lupin', models.BooleanField(default=False, verbose_name='Lupin')),
                ('molluscs', models.BooleanField(default=False, verbose_name='Molluscs')),
                ('allergens', models.ManyToManyField(blank=True, to='edible_products.allergen')),
            ],
        ),
        migrations.CreateModel(
            name='ProductWeightPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(help_text='Weight in grams')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weight_prices', to='edible_products.edibleproduct')),
            ],
        ),
    ]
