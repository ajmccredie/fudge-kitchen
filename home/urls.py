from django.urls import path
from . import views
from .views import FAQsView, SearchResultsView

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('our_story/', views.our_story, name='our_story'),
    path('faqs/', FAQsView.as_view(), name='faqs'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
]