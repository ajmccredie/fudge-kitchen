from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from decimal import Decimal
from .contexts import basket_contents
from core.models import CommonProduct
from edible_products.models import EdibleProduct, ProductWeightPrice
from merch.models import MerchProduct, TextOption
from profiles.models import SubscriptionProduct

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
    def post(self, request, item_id):
        print("Received data:", request.POST)  # Debug statement

        product_type = request.POST.get('product_type')
        print("Product type:", product_type)  # Debug statement
        
        if product_type == 'edible':
            product = get_object_or_404(EdibleProduct, pk=item_id)
            product_id = product.id
            name = product.name
            price = product.price
            image_url = product.image.url
        elif product_type == 'merch':
            product = get_object_or_404(MerchProduct, pk=item_id)
            product_id = product.id
            name = product.name
            price = product.price
            image_url = product.image.url
        elif product_type == 'subscription':
            product = get_object_or_404(SubscriptionProduct, pk=item_id)
            product_id = product.id
            name = "Annual Subscription"
            price = product.price
            image_url = product.image.url
        else:
            print("Invalid product type detected.")  # Debug statement
            messages.error(request, 'Invalid product type.')
            return redirect(reverse('basket:view_basket'))

        try:
            common_product = CommonProduct.objects.get(product_id=product_id, product_type=product_type)
            print("CommonProduct found:", common_product)  # Debug statement
        except CommonProduct.DoesNotExist:
            print(f"CommonProduct with Product ID {product_id} and type {product_type} does not exist.")
            messages.error(request, f"Product with ID {product_id} not found.")
            return redirect(reverse('basket:view_basket'))

        basket = request.session.get('basket', {})

        if product_type == 'edible':
            quantity = int(request.POST.get('quantity', 1))
            weight = int(request.POST.get('weight', 100))

            try:
                weight_price_obj = product.weight_prices.get(weight=weight)
                price = weight_price_obj.price
            except ProductWeightPrice.DoesNotExist:
                price = product.price

            if str(common_product.id) not in basket:
                basket[str(common_product.id)] = {'details': {}}

            if weight in basket[str(common_product.id)]['details']:
                basket[str(common_product.id)]['details'][weight] += quantity
            else:
                basket[str(common_product.id)]['details'][weight] = quantity

        elif product_type == 'merch':
            text_option_id = request.POST.get('text_option_id')
            quantity = int(request.POST.get('quantity', 1))

            if str(common_product.id) not in basket:
                basket[str(common_product.id)] = {'details': {}}

            if text_option_id in basket[str(common_product.id)]['details']:
                basket[str(common_product.id)]['details'][text_option_id] += quantity
            else:
                basket[str(common_product.id)]['details'][text_option_id] = quantity

        elif product_type == 'subscription':
            if request.user.profile.is_subscribed:
                messages.error(request, 'You already have an active subscription.')
                return redirect(reverse('basket:view_basket'))

            if str(common_product.id) in basket:
                messages.error(request, 'You cannot add more than one subscription to your basket.')
                return redirect(reverse('basket:view_basket'))

            basket = {k: v for k, v in basket.items() if CommonProduct.objects.get(pk=k).product_type != 'subscription'}
            basket[str(common_product.id)] = 1

        request.session['basket'] = basket
        request.session.modified = True
        messages.success(request, f'Added "{name}" to your basket.')
        return redirect(reverse('basket:view_basket'))

class ClearBasketView(View):
    def post(self, request, *args, **kwargs):
        if 'basket' in request.session:
            del request.session['basket']
            request.session.modified = True
            messages.success(request, 'Basket successfully emptied for you to reimagine the delicious things you want...')
        else:
            messages.info(request, 'Your basket is already empty.')
        return HttpResponseRedirect(reverse('basket:view_basket'))

class RemoveFromBasketView(View):
    @method_decorator(require_POST)
    def post(self, request, item_id):
        try:
            basket = request.session.get('basket', {})
            if str(item_id) in basket:
                del basket[str(item_id)]
                request.session.modified = True
                messages.success(request, "Item removed successfully.")
            else:
                messages.error(request, "Item not found in basket.")
        except Exception as e:
            messages.error(request, f"Error removing item: {str(e)}")
        return redirect(reverse('basket:view_basket'))


class AdjustBasketView(View):
    def post(self, request, item_id):
        quantity = int(request.POST.get('quantity'))
        basket = request.session.get('basket', {})

        if str(item_id) in basket:
            if quantity > 0:
                if 'details' in basket[str(item_id)]:
                    for detail in basket[str(item_id)]['details']:
                        basket[str(item_id)]['details'][detail] = quantity
                else:
                    basket[str(item_id)]['quantity'] = quantity
                messages.success(request, 'Updated quantity in your basket.')
            else:
                del basket[str(item_id)]
                if not basket:
                    del request.session['basket']
                messages.success(request, 'Removed item from your basket.')
            request.session.modified = True
        else:
            messages.error(request, 'Item not found in your basket.')

        return redirect(reverse('basket:view_basket'))