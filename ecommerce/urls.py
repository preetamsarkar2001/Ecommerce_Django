"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ecomm import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home,name="home"),
    path("login/", views.login1,name="login1"),
    path("signup/", views.signup,name="signup"),
    path("admin1/", views.admin1,name="admin1"),
    path("dashboard/", views.dashboard,name="dashboard"),
    path('analytics/', views.view_analytics, name='view_analytics'),
    path('add-category/', views.add_category, name='add_category'),
    path('list-category/', views.list_category, name='list_category'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-category/<int:pk>/', views.edit_category, name='edit_category'),
    path('delete-category/<int:pk>/', views.delete_category, name='delete_category'),
    path('list-product/', views.list_product, name='list_product'),
    path('update-product/<int:pk>/', views.update_product, name='update_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('upload-slider/', views.upload_slider, name='upload_slider'),
    path('update-cart-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove-cart-item/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
  
    path('view-orders/', views.view_orders, name='view_orders'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:cat_id>/', views.category_detail, name='category_detail'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html'), name='change_password'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('order-history/', views.order_history, name='order_history'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('download-receipt/<int:order_id>/', views.download_receipt, name='download_receipt'),
    path('add-feedback/<int:order_id>/', views.add_feedback, name='add_feedback'),
    # path('download-report/', views.download_report, name='download_report'),
    
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    path('logout/', views.user_logout, name='logout')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
