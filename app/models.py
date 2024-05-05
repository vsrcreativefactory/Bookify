from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Create your models here.

CATEGORY_CHOICES=(
    ('FN','Fiction'),
    ('NF','Non-fiction'),
    ('BY','Biography'),
    ('SC','Science'),
    ('TR','Thriller'),
    ('RO','Romance'),
    ('PO','Poetry'),
)
class Product(models.Model):
    title = models.CharField(max_length=100)
    author= models.CharField(max_length=20, default='Unknown')
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    language = models.CharField(max_length=50, default='English')
    year = models.IntegerField(default=2023)
    product_image = models.ImageField(upload_to='product')
    stock = models.PositiveIntegerField(default=0)
    discount = models.FloatField(default=0)
    
    def __str__(self):
        return self.title
    
class Customer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #user= models.ForeignKey(User, on_delete=models.CASCADE)
    name= models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    zipcode = models.CharField(max_length=6)
    state = models.CharField(max_length=50)
    #email verification
    otp = models.CharField(max_length=6, blank=True, null=True)
    #uid = models.CharField(default=f'{uuid.uuid4}', max_length=200)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.discounted_price
    
class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=100, default='COD')
    refunded = models.BooleanField(default=False)

class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10, unique=True)
    discount = models.FloatField()
    lower_limit = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    upper_limit = models.DecimalField(max_digits=8, decimal_places=2, default=10000)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.coupon_code
    
class CouponUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'coupon']

    def __str__(self):
        return f'{self.user.username} - {self.coupon.coupon_code}'

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way','On the way'),
    ('Delivered','Delivered'),
    ('Cancelled','Cancelled'),
    ('Pending','Pending'),
)
    
class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default="" , null=True)
    return_reason = models.TextField(blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)

class ProductOffer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_percentage = models.FloatField(verbose_name=_('Discount Percentage'))

class WalletTransaction(models.Model):
    TRANSACTION_TYPES = (
        ('REFUND', 'Refund'),
        ('PURCHASE', 'Purchase'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.id} | {self.type} | {self.date} | {self.amount}"