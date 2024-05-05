from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from .views import cancel_order, delete_address, return_order, search_results


urlpatterns = [
    #path('',views.home),
    path('', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('home/', views.home, name="home"),
    path('about/',views.about, name="about"),
    path('contact/',views.contact, name="contact"),

    #product side
    path('category/<slug:val>',views.CategoryView.as_view(),name="category"),
    path('product-detail/<int:pk>',views.ProductDetail.as_view(),name="product-detail"),
    path('category-title/<val>',views.CategoryTitle.as_view(),name="category-title"),
    
    #user side
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("address/", views.address, name="address"),
    path('updateAddress/<int:pk>', views.updateAddress.as_view(), name='updateAddress'),
    path('delete_address/<int:pk>/', delete_address, name='delete-address'),  

    #cart functionalities
    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('cart/', views.show_cart, name="showcart"),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),

    #order side
    path('checkout/', views.checkout.as_view(), name="checkout"),
    path('paymentdone/', views.payment_done, name="paymentdone"),
    path('cash-on-delivery/', views.checkout.as_view(), name='cash-on-delivery'),
    path('pay-from-wallet/', views.checkout.as_view(), name='pay-from-wallet'),
    path('order-success/',views.order_success, name="order-success"),
    path('orders/',views.orders, name='orders'),

    path('wallet/',views.wallet, name='wallet'),
    path('add-to-wallet/', views.add_to_wallet, name='add-to-wallet'),
    path('create-razorpay-order/', views.create_razorpay_order, name='create_razorpay_order'),
    path('process_payment/', views.process_payment, name='process_payment'),

    #path('wallet-success/', views.WalletSuccess.as_view(), name='wallet-success'),

    path('cancel-order/<int:order_id>/', cancel_order, name='cancel-order'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete-order'),
    path('return_order/<int:order_id>/', return_order, name='return-order'),
    path('cancel-return/<int:order_id>/', views.cancel_return, name='cancel-return'),
    
    path('hrishi/',views.hrishi,name='hrishi'),
    path('invoice/',views.invoice, name='invoice'),
    path('download_pdf/', views.download_pdf, name='download_pdf'),

    #wishlist
    path('pluswishlist/', views.plus_wishlist),
    path('minuswishlist/', views.minus_wishlist),
    path('wishlist/', views.show_wishlist, name="showwishlist"),
    path('delete-from-wishlist/<int:product_id>/', views.delete_from_wishlist, name="delete_from_wishlist"),

#https://www.youtube.com/watch?v=qwFBXuEeg1U&list=PPSV
#https://github.com/vishnu2044/Bookstall-e-commerce-webapp/blob/main/

    #login authentication
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/',auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', views.user_logout, name='logout'),

    #change password
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone'), name='passwordchange'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    
    #otp authentication
    path("subscribe/",views.subscribe, name="subscribe"),
    path('otp-verification/', views.otp_verification, name='otp_verification'),

    #forget password
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='app/forget_password/password_reset.html', form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done',auth_view.PasswordResetDoneView.as_view(template_name='app/forget_password/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='app/forget_password/password_reset_confirm.html', form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='app/forget_password/password_reset_complete.html'),name='password_reset_complete'),

    #search
    path('search/', views.search_results, name='search_results'),
    #coupon
    #path('coupons/', views.view_coupons, name='view_coupons'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)