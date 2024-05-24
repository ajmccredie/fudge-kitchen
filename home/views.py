from django.shortcuts import render, redirect
from .models import OurStory
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import InquiryForm
from django.views import View
from django.db.models import Q
from core.models import CommonProduct
from edible_products.models import EdibleProduct
from merch.models import MerchProduct
from profiles.models import SubscriptionProduct

# Create your views here.

def index(request):
    """ A view to return the index page """
    
    return render(request, 'home/index.html') 


def our_story(request):
    story = OurStory.objects.first() 
    context = {'story': story}
    return render(request, 'home/our_story.html', context)


class FAQsView(TemplateView):
    template_name = 'home/faqs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['form'] = InquiryForm(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.user = request.user
            inquiry.save()
            messages.success(request, 'Thank you for messaging our admin')
            return redirect('home:faqs')
        return self.render_to_response(self.get_context_data(form=form))


class SearchResultsView(View):
    template_name = 'home/search_results.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        if query:
            # Searching edible products
            edible_products = EdibleProduct.objects.filter(
                Q(name__icontains=query) | 
                Q(flavour__icontains=query)
            )

            # Searching merch products
            merch_products = MerchProduct.objects.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query)
            )

            # Searching subscription products
            subscription_products = SubscriptionProduct.objects.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query)
            )
        else:
            edible_products = merch_products = subscription_products = None

        context = {
            'edible_products': edible_products,
            'merch_products': merch_products,
            'subscription_products': subscription_products,
            'query': query
        }
        return render(request, self.template_name, context)
