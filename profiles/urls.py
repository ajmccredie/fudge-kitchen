from django.urls import path
from .views import EditProfileView, ProfileView

urlpatterns = [
 #   path('edit/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
