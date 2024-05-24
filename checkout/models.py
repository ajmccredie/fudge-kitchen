import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings
from decimal import Decimal

from django_countries.fields import CountryField

from profiles.models import Profile
from edible_products.models import EdibleProduct, ProductWeightPrice
from merch.models import MerchProduct, TextOption
from profiles.models import SubscriptionProduct
from core.models import Product, CommonProduct


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_basket = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')
    dispatched = models.BooleanField(default=False)

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.user_profile and self.user_profile.is_subscribed:
            self.delivery_cost = 0
        else:
            self.delivery_cost = 3
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    edible_product = models.ForeignKey(EdibleProduct, null=True, blank=True, on_delete=models.CASCADE)
    merch_product = models.ForeignKey(MerchProduct, null=True, blank=True, on_delete=models.CASCADE)
    subscription_product = models.ForeignKey(SubscriptionProduct, null=True, blank=True, on_delete=models.CASCADE)
    product_type = models.CharField(max_length=20, null=True, blank=True)

    weight = models.IntegerField(null=True, blank=True)  # Stores the selected weight
    quantity = models.IntegerField(null=False, blank=False, default=0)
    selected_text = models.ForeignKey(TextOption, null=True, blank=True, on_delete=models.SET_NULL)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)
    made = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            if self.product_type == 'edible' and self.weight:
                price_per_unit = self.edible_product.get_price_for_weight(self.weight)
                print(price_per_unit)
                if price_per_unit is None:
                    price_per_unit = Decimal('7.00')
                self.lineitem_total = price_per_unit * Decimal(self.quantity)
            elif self.product_type == 'merch':
                self.lineitem_total = self.merch_product.price * Decimal(self.quantity)
            elif self.product_type == 'subscription':
                self.lineitem_total = self.subscription_product.price * Decimal(self.quantity)

        super().save(*args, **kwargs)

    def __str__(self):
        if self.product_type == 'edible':
            return f'{self.edible_product.flavour} ({self.weight}g) on order {self.order.order_number}'
        elif self.product_type == 'merch':
            text = f" - {self.selected_text.text}" if self.selected_text else ""
            return f'{self.merch_product.name}{text} on order {self.order.order_number}'
        else:
            return f'Subscription product on order {self.order.order_number}'