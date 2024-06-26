from django.urls import path
from .views import (
    DashboardView, EdibleProductListView, EdibleProductCreateView,
    EdibleProductUpdateView, EdibleProductDeleteView, MerchProductListView,
    MerchProductCreateView, MerchProductUpdateView, MerchProductDeleteView,
    OrderListView, OrderDetailView, mark_order_dispatched, mark_item_made,
    delete_order, InquiryListView, InquiryDetailView, MarkInquiryDealtWithView,
    ClearBasketCacheView, SubscriptionProductListView,
    SubscriptionProductCreateView, SubscriptionProductUpdateView,
    SubscriptionProductDeleteView, SubscribedUsersListView,
    UpdateSubscriptionStatusView, SubscriptionManagementView,
    NewsletterRecipientsView, SubProfileDetailView
)

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name='home'),
    path(
        'products/',
        EdibleProductListView.as_view(),
        name='edible_product_list'
    ),
    path(
        'products/new/', EdibleProductCreateView.as_view(),
        name='edible_product_create'
    ),
    path(
        'products/edit/<int:pk>/', EdibleProductUpdateView.as_view(),
        name='edible_product_edit'
    ),
    path(
        'products/delete/<int:pk>/', EdibleProductDeleteView.as_view(),
        name='edible_product_delete'
    ),
    path('merch/', MerchProductListView.as_view(), name='merch_product_list'),
    path(
        'merch/new/', MerchProductCreateView.as_view(),
        name='merch_product_create'
    ),
    path(
        'merch/<int:pk>/edit/', MerchProductUpdateView.as_view(),
        name='merch_product_update'
    ),
    path(
        'merch/<int:pk>/delete/', MerchProductDeleteView.as_view(),
        name='merch_product_delete'
    ),
    path('order_list/', OrderListView.as_view(), name='order_list'),
    path(
        'order_list/<int:pk>/', OrderDetailView.as_view(),
        name='order_details'
    ),
    path(
        'order_list/<int:order_id>/dispatched/', mark_order_dispatched,
        name='mark_order_dispatched'
    ),
    path(
        'order_list/items/<int:item_id>/made/', mark_item_made,
        name='mark_item_made'
    ),
    path(
        'order_list/<int:order_id>/delete/', delete_order,
        name='delete_order'
    ),
    path('inquiries/', InquiryListView.as_view(), name='inquiries_list'),
    path(
        'inquiries/<int:pk>/', InquiryDetailView.as_view(),
        name='inquiries_detail'
    ),
    path(
        'inquiries/<int:pk>/dealt_with/', MarkInquiryDealtWithView.as_view(),
        name='mark_inquiry_dealt_with'
    ),
    path(
        'clear_basket_cache/', ClearBasketCacheView.as_view(),
        name='clear_basket_cache'
    ),
    path(
        'subscriptions/', SubscriptionProductListView.as_view(),
        name='subscription_product_list'
    ),
    path(
        'subscriptions/management/', SubscriptionManagementView.as_view(),
        name='subscription_management'
    ),
    path(
        'subscriptions/new/', SubscriptionProductCreateView.as_view(),
        name='subscription_product_create'
    ),
    path(
        'subscriptions/<int:pk>/edit/',
        SubscriptionProductUpdateView.as_view(),
        name='subscription_product_update'
    ),
    path(
        'subscriptions/<int:pk>/delete/',
        SubscriptionProductDeleteView.as_view(),
        name='subscription_product_delete'
    ),
    path(
        'subscribed_users/', SubscribedUsersListView.as_view(),
        name='subscribed_users_list'
    ),
    path(
        'subscribed_users/<int:pk>/update_status/',
        UpdateSubscriptionStatusView.as_view(),
        name='update_subscription_status'
    ),
    path(
        'profile/<int:pk>/',
        SubProfileDetailView.as_view(),
        name='sub_profile_detail'
    ),
    path(
        'newsletter_recipients/',
        NewsletterRecipientsView.as_view(),
        name='newsletter_recipients'
    ),
]
