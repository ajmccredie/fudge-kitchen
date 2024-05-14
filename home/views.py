from django.shortcuts import render, redirect
from .models import OurStory
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import InquiryForm

# Create your views here.

def index(request):
    """ A view to return the index page """
    
    return render(request, 'home/index.html') 


def our_story(request):
    story = OurStory.objects.first() 
    context = {'story': story}
    return render(request, 'home/our_story.html', context)


class FAQsView(LoginRequiredMixin, TemplateView):
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