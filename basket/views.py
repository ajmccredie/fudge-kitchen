from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse, HttpResponse
from .contexts import basket_contents
from decimal import Decimal, InvalidOperation
from edible_products.models import EdibleProduct, ProductWeightPrice
from merch.models import MerchProduct, ColourVariation, TextOption

class BasketView(View):
    def get(self, request, *args, **kwargs):
        context_data = basket_contents(request)
        basket_items = context_data.get('basket_items', [])
        total = context_data.get('total', Decimal('0.00'))
        product_count = context_data.get('product_count')
        delivery = context_data.get('delivery')
        grand_total = context_data.get('grand_total')
        is_subscribed = False
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            is_subscribed = request.user.profile.is_subscribed  

        context = {
            'is_subscribed': is_subscribed,
                'basket_items': basket_items,
                'total': total,
                'product_count': product_count,
                'delivery': delivery,
                'grand_total': grand_total,
            }
        return render(request, 'basket/basket.html', context)


class AddToBasketView(View):
    def post(self, request: HttpRequest, item_id):
        """Add a quantity of the specified product to the shopping basket."""
        quantity = int(request.POST.get('quantity'))
        flavour = request.POST.get('flavour')
        redirect_url = request.POST.get('redirect_url', reverse('view_basket'))
        product = get_object_or_404(EdibleProduct, pk=item_id)
        weight = int(request.POST.get('weight', '100')) 

        try:
            weight_price_obj = product.weight_prices.get(weight=weight)
            price = weight_price_obj.price
        except ProductWeightPrice.DoesNotExist:
            price = product.price

        basket = request.session.get('basket', {})
        item_key = f"edible-{item_id}-{flavour}-{weight}"

        if item_key in basket:
            basket[item_key]['quantity'] += quantity
        else:
            basket[item_key] = {
                'product_id': item_id,
                'product_type': 'edible',
                'flavour': flavour,
                'weight': weight,
                # 'quantity': quantity,
                'quantity': basket.get(item_key, {}).get('quantity', 0) + quantity,
                'price': str(price),
                'image_url': product.image.url if product.image else None,
                'name': product.name
            }

        request.session['basket'] = basket
        request.session.modified = True
        messages.success(request, f'Added "{product.flavour}" to your basket.')
        return redirect(redirect_url)


# class AddToBasketView(View):
#     def post(self, request: HttpRequest, *args, **kwargs):
#         product_id = request.POST.get('product_id')
#         product_type = request.POST.get('product_type', 'edible')
#         quantity = int(request.POST.get('quantity', 1))
#         redirect_url = request.POST.get('redirect_url', reverse('view_basket'))
#         basket = request.session.get('basket', {})

#         if product_type == 'edible':
#             product = get_object_or_404(EdibleProduct, pk=product_id)
#             weight = int(request.POST.get('weight'))
#             item_key = f"edible-{product_id}-{weight}"
#             price = product.weight_prices.get(weight=weight).price
#         elif product_type == 'merch':
#             product = get_object_or_404(MerchProduct, pk=product_id)
#             colour_id = request.POST.get('colour')
#             text_option_id = request.POST.get('text_option', None)
#             item_key = f"merch-{product_id}-{colour_id}-{text_option_id if text_option_id else ''}"
#             price = product.price

#         if item_key in basket:
#             basket[item_key]['quantity'] += quantity
#         else:
#             basket[item_key] = {
#                 'product_type': product_type,
#                 'quantity': quantity,
#                 'price': str(price),
#                 'colour_id': colour_id if product_type == 'merch' else None,
#                 'text_option_id': text_option_id if product_type == 'merch' else None,
#                 'weight': weight if product_type == 'edible' else None,
#             }

#         request.session['basket'] = basket
#         request.session.modified = True
#         messages.success(request, f'Added {quantity} {product.name} to your basket.')
#         return redirect(redirect_url)


class AddMerchToBasketView(View):
    def post(self, request, item_id):
        merch = get_object_or_404(MerchProduct, pk=item_id)
        colour_id = request.POST.get('colour')
        text_option_id = request.POST.get('text_option', None)
        quantity = int(request.POST.get('quantity'))

        basket = request.session.get('basket', {})
        item_key = f"merch-{item_id}-{colour_id}-{text_option_id if text_option_id else ''}"
        
        if item_key in basket:
            basket[item_key]['quantity'] += quantity
        else:
            basket[item_key] = {
                'product_id': item_id,
                'product_type': 'merch',
                'colour_id': colour_id,
                'text_option_id': text_option_id,
                # 'quantity': quantity,
                'quantity': basket.get(item_key, {}).get('quantity', 0) + quantity,
                'price': str(merch.price),
                'image_url': merch.image.url if merch.image else None,
                'name': merch.name
            }

        request.session['basket'] = basket
        request.session.modified = True
        messages.success(request, f'Added {quantity} {merch.name} to your basket.')
        return redirect(reverse('view_basket'))


class ClearBasketView(View):
    def post(self, request, *args, **kwargs):
        if 'basket' in request.session:
            del request.session['basket']
            request.session.modified = True
            messages.success(request, 'Basket successfully emptied for you to reimagine the delicious things you want...')
        else:
            messages.info(request, 'Your basket is already empty.')
        return HttpResponseRedirect(reverse('view_basket'))


class RemoveFromBasketView(View):
    def post(self, request, item_id):
        basket = request.session.get('basket', {})
        try:
            if item_id in basket:
                del basket[item_id]
                if not basket:
                    del request.session['basket']
                request.session.modified = True
                messages.success(request, 'Item removed from your basket.')
            else:
                messages.error(request, 'Item not found in your basket.')
        except Exception as e:
            messages.error(request, f'Error removing item: {str(e)}')
        return redirect('view_basket')

# class AdjustBasketView(View):
#     def post(self, request, item_id):
#         basket = request.session.get('basket', {})
#         quantity = int(request.POST.get('quantity'))

#         if 'edible' in item_id:
#             flavour = request.POST.get('flavour')
#             weight = int(request.POST.get('weight', 100)) 
#             item_key = f"edible-{item_id}-{flavour}-{weight}"
#         elif 'merch' in item_id:
#             item_key = f"merch-{item_id}-{colour_id}-{text_option_id if text_option_id else ''}"
#         else:
#             item_key = item_id

#         if item_key in basket:
#             if quantity > 0:
#                 basket[item_key]['quantity'] = quantity
#                 messages.success(request, f'Updated quantity in your basket.')
#             else:
#                 del basket[item_key]
#                 if not basket:
#                     del request.session['basket']
#                 messages.success(request, 'Removed item from your basket.')
#             request.session.modified = True
#         else:
#             messages.error(request, 'Item not found in your basket.')

#         return HttpResponseRedirect(reverse('view_basket'))

class AdjustBasketView(View):
    def post(self, request, item_id):
        basket = request.session.get('basket', {})
        quantity = int(request.POST.get('quantity'))

        if item_id in basket:
            if quantity > 0:
                basket[item_id]['quantity'] = quantity
                messages.success(request, 'Updated quantity in your basket.')
            else:
                del basket[item_id]
                if not basket:
                    del request.session['basket']
                messages.success(request, 'Removed item from your basket.')
            request.session.modified = True
        else:
            messages.error(request, 'Item not found in your basket.')

        return HttpResponseRedirect(reverse('view_basket'))


