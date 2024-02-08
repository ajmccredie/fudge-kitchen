from django.shortcuts import render
from django.views.generic import View

# Define the class-based view
class BasketView(View):
    def get(self, request, *args, **kwargs):
        """ A view that renders the bag contents page """
        return render(request, 'basket/basket.html')
