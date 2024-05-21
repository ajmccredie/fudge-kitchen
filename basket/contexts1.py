from django.conf import settings
from django.shortcuts import get_object_or_404
from edible_products.models import EdibleProduct, ProductWeightPrice
from profiles.models import Profile
from merch.models import MerchProduct, ColourVariation, TextOption
from decimal import Decimal


def basket_contents(request):
    basket_items = {}
    total = Decimal('0.00')
    product_count = 0
    basket = request.session.get('basket', {})

    product_handlers = {
        'edible': handle_edible_product,
        'merch': handle_merch_product,
    }

    for item_key, item_data in basket.items():
        product_type = item_data.get('product_type', 'default_type')
        handler = product_handlers.get(product_type)
        if handler:
            result = handler(item_key, item_data)
            if result:
                basket_items[item_key] = result['item']
                total += result['subtotal']
                product_count += result['quantity']

    delivery = calculate_delivery(total, request.user)

    context = {
        'basket_items': basket_items,
        'total': total,
        'grand_total': total + delivery,
        'product_count': product_count,
        'delivery': delivery,
    }

    return context

def handle_edible_product(item_key, item_data):
    product = get_object_or_404(EdibleProduct, pk=item_data['product_id'])
    weight = int(item_data.get('weight', '400'))

    try:
        weight_price = ProductWeightPrice.objects.get(product=product, weight=weight)
        price = weight_price.price
    except ProductWeightPrice.DoesNotExist:
        price = product.price

    quantity = item_data.get('quantity', 1)
    subtotal = Decimal(quantity) * Decimal(price)

    return {
        'item': {
            'product_id': product.id,
            'quantity': quantity,
            'product': product,
            'product_type': 'edible',
            'price': price,
            'subtotal': subtotal,
            'name': product.name,
            'image_url': product.image.url if product.image else None,
            'flavour': product.flavour,
            'weight': weight
        },
        'subtotal': subtotal,
        'quantity': quantity
    }

def handle_merch_product(item_key, item_data):
    product = get_object_or_404(MerchProduct, pk=item_data['product_id'])
    quantity = item_data.get('quantity', 1)
    price = product.price
    subtotal = Decimal(quantity) * price

    colour_variation = None
    text_option = None
    if 'colour_id' in item_data:
        colour_variation = ColourVariation.objects.filter(id=item_data['colour_id']).first()
    if 'text_option_id' in item_data:
        text_option = TextOption.objects.filter(id=item_data['text_option_id']).first()
        print(text_option)

    item_dict = {
        'product_id': product.id,
        'quantity': quantity,
        'product': product,
        'price': price,
        'subtotal': subtotal,
        'product_type': 'merch',
        'name': product.name,
        'image_url': product.image.url if product.image else None
    }

    if text_option:
        item_dict['text_option'] = text_option.text
        item_dict['text_option_image'] = text_option.image.url if text_option.image else None

    return {
        'item': item_dict,
        'subtotal': subtotal,
        'quantity': quantity
    }


def calculate_delivery(total, user):
    delivery = Decimal(settings.DEFAULT_DELIVERY_CHARGE) if total > Decimal('0.00') else Decimal('0.00')
    if user and user.is_authenticated:
        profile = Profile.objects.filter(user=user).first()
        if profile and profile.is_subscribed:
            delivery = Decimal('0.00')
    return delivery
