from django.contrib import admin
from . models import Coupon, Product, Customer, Cart, Payment, OrderPlaced, ProductOffer, Wishlist
from django.contrib.auth.models import Group

# Register your models here.

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','author','discounted_price','category','product_image']


@admin.register(Customer)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality','city','state','zipcode']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']


@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']


@admin.register(OrderPlaced)
class OrderPlaceModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','ordered_date','status','payment']


@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product']
    

@admin.register(Coupon)
class CouponModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'coupon_code', 'discount', 'lower_limit', 'upper_limit', 'active']
    
@admin.register(ProductOffer)
class ProductOfferAdmin(admin.ModelAdmin):
    list_display = ['product', 'discount_percentage']
    
admin.site.unregister(Group)