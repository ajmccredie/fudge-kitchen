from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import EdibleProduct


@receiver(post_save, sender=EdibleProduct)
def product_updated(sender, instance, created, **kwargs):
    if not created:
        print(f'Product {instance.id} updated!')


@receiver(m2m_changed, sender=EdibleProduct.allergens.through)
def allergens_updated(sender, instance, action, pk_set, **kwargs):
    if action == "post_add" or action == "post_remove":
        allergen_names = [
            allergen.name for allergen in instance.allergens.all()
            ]
        print(f'Allergens updated for product {instance.id}: {allergen_names}')
