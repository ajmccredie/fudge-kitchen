from django.urls import path
from .views import EditProfileView, ProfileView, DeleteProfileView, OrderDetailView

urlpatterns = [
    path('edit/', EditProfileView.as_view(), name='edit_profile'),
    path('delete/', DeleteProfileView.as_view(), name='delete_account'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
]
