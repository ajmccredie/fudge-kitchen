from django.shortcuts import render
from .models import OurStory

# Create your views here.

def index(request):
    """ A view to return the index page """
    
    return render(request, 'home/index.html') 


def our_story(request):
    story = OurStory.objects.first() 
    context = {'story': story}
    return render(request, 'home/our_story.html', context)