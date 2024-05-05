from django.urls import path
from . views import *
from django.contrib import admin
from . import views
from .views import manage_products, manage_users

urlpatterns = [
    path('', admin_login, name="admin_login"),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/',dashboard,name="dashboard"),

    path('admin_home/',admin_home,name="admin_home"),
    path('adminprofile/',adminprofile,name="adminprofile"),

    path('all_products/',all_products,name="all_products"),
    path('add_products/',add_products,name="add_products"),
    path('edit_products/<int:pk>/',edit_products,name="edit_products"),
    path('manage_products/', manage_products, name='manage_products'),
    path('delete_product/<int:pk>/', delete_product, name='delete_product'),

    path('all_users/',all_users,name="all_users"),
    path('add_users/',add_users,name="add_users"),
    path('edit_users/<int:pk>/', edit_users, name="edit_users"),
    path('manage_users/', manage_users, name='manage_users'),
    path('delete_user/<int:pk>/', delete_user, name='delete_user'),

    path('block_user/<int:pk>/', views.block_user, name='block_user'),
    path('unblock_user/<int:pk>/', views.unblock_user, name='unblock_user'),

    path('all_categories/',all_categories,name="all_categories"),
    path('add_categories/',add_categories,name="add_categories"),
    path('edit_categories/<int:pk>/', edit_categories, name="edit_categories"),
    #path('manage_categories/', manage_categories, name='manage_categories'),
    path('delete_category/<int:pk>/', views.delete_category, name='delete_category'),

    path('list_orders/', list_orders, name='list_orders'),
    path('manage_orders/', views.manage_orders, name='manage_orders'),
    path('edit_order/<int:pk>/', views.edit_order, name='edit_order'),
    path('cancel_order/<int:pk>/', views.cancel_order, name='cancel_order'),
    path('return-requests/', views.return_requests, name='return-requests'),
    path('admin-approval/<int:order_id>/', views.admin_approval, name='admin-approval'),

    path('all_coupons/',all_coupons,name="all_coupons"),
    path('add_coupons/', views.add_coupons, name='add_coupons'),
    path('edit_coupons/<int:pk>/', views.edit_coupons, name='edit_coupons'),
    path('delete_coupon/<int:pk>/', views.delete_coupon, name='delete_coupon'),

    path('product-offers/', views.list_product_offers, name='list_product_offers'),
    path('product-offers/add/', views.add_product_offer, name='add_product_offer'),
    path('product-offers/delete/<int:pk>/', views.delete_product_offer, name='delete_product_offer'),

    path('report-pdf-order/', views.report_pdf_order, name='report_pdf_order'),

    path('sales_report/', views.sales_report, name="sales_report"),
    path('bardiagram/', views.bardiagram, name='bardiagram'),
]

