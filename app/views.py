from profile import Profile
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
import razorpay
from . models import Coupon, CouponUsage, Customer, OrderPlaced, Payment, Product, Cart, ProductOffer, Wallet, WalletTransaction, Wishlist
from . forms import CustomerRegistrationForm, CustomerProfileForm, SubscribeForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
#after otp implimentation
from django.contrib.auth.models import User
import random
import re
import datetime
from .helper import MessageHandler
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.cache import never_cache
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from django.http import FileResponse
from reportlab.lib.pagesizes import A4
import io
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def home(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/home.html",locals())

def about(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/about.html",locals())

def contact(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/contact.html",locals())

@never_cache
def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')

class CategoryView(View):
    def get(self,request,val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        paginator = Paginator(product, 10)  # Change 10 to your desired number of items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,"app/category.html",locals())

@method_decorator(login_required,name='dispatch')
class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product)& Q(user=request.user))
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request,"app/product_detail.html",locals())

class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request,"app/category.html",locals())
    
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,'app/registration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save() # Save the user instance for twilio
            
            messages.success(request,"Congratulations ! account created successfully")
            return redirect('subscribe')
        else:
            messages.warning(request,"Invalid Input data ! Try again after refresh")
            return render(request,'app/registration.html',locals())
        
@method_decorator(login_required,name='dispatch')        
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request,'app/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.user = user  # Set the user field separately
            reg.save()
            messages.success(request,"Done...Profile saved successfully")
        else:
            messages.warning(request,"Invalid input data")
        return render(request,'app/profile.html',locals())

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/address.html',locals())

@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)#for automatically fill data
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/updateaddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations ! Profile updated Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")

@login_required
def delete_address(request, pk):
    # Ensure that the address belongs to the logged-in user
    address = get_object_or_404(Customer, pk=pk, user=request.user)
    
    if request.method == 'POST':
        address.delete()
        messages.success(request, "Address deleted successfully.")
        return redirect('address')
    else:
        return redirect('address')

@login_required   
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    #product = get_object_or_404(Product, id=product_id)
    product = Product.objects.get(id=product_id)
    #offer
    # Fetch active product offers
    active_offers = ProductOffer.objects.filter(product=product)
    # Apply discounts from active offers
    discounted_price = product.selling_price  # Initialize with the original price
    for offer in active_offers:
        discounted_price -= (product.selling_price * offer.discount_percentage / 100)
        
    cart_items_count = Cart.objects.filter(user=user).count()
    if cart_items_count < 5:
        cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        #check if the product is exists in wishlist
        wishlist_item = Wishlist.objects.filter(user=user, product=product)
        if wishlist_item.exists():
            wishlist_item.delete()
        # Check if the cart item was created or updated
        if created or (cart_item.quantity < product.stock and cart_item.quantity < 3): # Assuming 5 is the max quantity per person
            if not created:
                cart_item.quantity += 1
            cart_item.save()
            #messages.success(request, "Product added to cart successfully!")
        else:
            messages.error(request, "Cannot add more of this product to the cart.")
    else:
        messages.error(request, "You can only add up to 5 products to the cart.")
    return redirect("/cart", {'active_offers': active_offers})

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
        offer = (p.product.discounted_price * 10 / 100)
    totalamount = (amount + 60) - offer

    # Fetch active product offers for all products in the cart
    active_offers = {}
    for cart_item in cart:
        product_offers = ProductOffer.objects.filter(product=cart_item.product)
        active_offers[cart_item.product.id] = product_offers

    product_stocks = {}
    for a in cart:
        product_stocks[a.product.id] = a.product.stock
    # Coupon code handling
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code)
            if coupon.lower_limit <= totalamount <= coupon.upper_limit:
                # Check if the coupon hasn't been used yet
                if not CouponUsage.objects.filter(user=user, coupon=coupon).exists():
                    if coupon.discount <= totalamount:
                        # Apply discount
                        totalamount -= coupon.discount
                        # Mark coupon as used
                        CouponUsage.objects.create(user=user, coupon=coupon)
                        messages.success(request, f'Coupon "{coupon_code}" applied successfully. Discount of {coupon.discount} applied.')
                    else:
                        messages.error(request, f'Coupon discount ({coupon.discount}) cannot exceed total amount ({totalamount}).')
                else:
                    messages.error(request, f'You have already used the coupon code "{coupon_code}".')
            else:
                messages.error(request, f'Your total amount does not meet the conditions to use the coupon code "{coupon_code}".')
        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid Coupon Code.')
    try:
        wallet = Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        wallet = None
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    coupons = Coupon.objects.all()
    # Fetch messages
    all_messages = messages.get_messages(request)
    return render(request, 'app/addtocart.html',{'cart': cart, 'totalamount': totalamount, 'wallet': wallet, 'totalitem': totalitem, 'wishitem': wishitem, 'coupons': coupons, 'all_messages': all_messages, 'product_stocks': product_stocks, 'active_offers': active_offers})

def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        print(c.quantity)
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 60
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 60
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 60
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

class checkout(View):
    def get(self, request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 60
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount":razoramount, "currency":"INR","receipt":"order-rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status,
                payment_method='Razorpay'
            )
            payment.save()
        # wallet = Wallet.objects.get(user=user)
        return render(request, 'app/checkout.html', locals())
    
    #starts
    def post(self, request):
        payment_method = request.POST.get('payment_method')
        if payment_method == 'cod':
            return self.cash_on_delivery(request)
        elif payment_method == 'wallet':
            return self.pay_from_wallet(request)
    
    def cash_on_delivery(self,request):
        if request.method == 'POST':
            # Retrieve necessary data from the request
            cust_id = request.POST.get('custid')
            user = request.user
            customer = Customer.objects.get(id=cust_id)
            # Process COD payment
            cart_items = Cart.objects.filter(user=user)
            for cart_item in cart_items:
                OrderPlaced.objects.create(
                    user=user,
                    customer=customer,
                    product=cart_item.product,
                    quantity=cart_item.quantity,   
                )
                cart_item.product.stock -= cart_item.quantity
                cart_item.product.save()
                cart_item.delete()
            # Redirect to order success page
            return redirect("order-success")
        else:
            return redirect("checkout")
        
    def pay_from_wallet(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 60
        # Check if the wallet balance is sufficient
        wallet = Wallet.objects.get(user=user)
        if wallet.balance >= totalamount:
            # Deduct the order amount from the wallet balance
            wallet.balance -= totalamount
            wallet.save()
            # Create a payment record
            payment = Payment.objects.create(
                user=user,
                amount=totalamount,
                payment_method='Wallet'  # Indicate payment method
            )
            # Save the order and related items
            with transaction.atomic():
                cust_id = request.POST.get('custid')
                user = request.user
                customer = Customer.objects.get(id=cust_id)
                cart_items = Cart.objects.filter(user=user)
                for cart_item in cart_items:
                    OrderPlaced.objects.create(
                        user=user,
                        customer=customer,
                        product=cart_item.product,
                        quantity=cart_item.quantity, 
                        payment=payment,  
                    )
                    cart_item.product.stock -= cart_item.quantity
                    cart_item.product.save()
                    cart_item.delete()
            WalletTransaction.objects.create(
                user=user,
                type='PURCHASE',
                amount=totalamount
            )
            return redirect("order-success")
        else:
            messages.error(request, "Your wallet balance is insufficient.")
        return redirect("checkout")

@login_required    
def payment_done(request):
    order_id = request.GET.get('order_id')
    print("first order_id",order_id)
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    user = request.user
    customer = Customer.objects.get(id=cust_id)
    #to update payment status & payment id
    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    print("order id: ", payment.razorpay_order_id)
    print(order_id)
    #to save order details
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.product.stock -= c.quantity
        c.product.save()
        c.delete()
    return redirect("order-success")

@login_required
def order_success(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/order-success.html")

#invoice
@login_required
def invoice(request):
    user = request.user
    customer = Customer.objects.filter(user=user).first()
    latest_order = OrderPlaced.objects.filter(user=user).order_by('-id').first()
    if latest_order:
        selected_address = latest_order.customer
        today = datetime.date.today()
        latest_invoice = OrderPlaced.objects.latest('id')
        invoice_number = latest_invoice.id + 100
        if latest_order.payment:
            payment_method = latest_order.payment.payment_method
        else:
            payment_method = "Cash on Delivery"
        total_amount = latest_order.total_cost
        last_payment = Payment.objects.filter(user=user, paid=True).order_by('-id').first()
        if last_payment:
            grand_total = total_amount + 60
        else:
            grand_total = 0
        # Fetch all products in the latest order
        ordered_items = []
        for order in OrderPlaced.objects.filter(user=user, id=latest_order.id).select_related('product'):
            ordered_items.append({
                'title': order.product.title,
                'category': order.product.category,
                'quantity': order.quantity,
                'final_price': order.product.discounted_price * order.quantity
            })
        if ordered_items:
            context = {
                'user': user,
                'customer': customer,
                'selected_address': selected_address,
                'today': today,
                'invoice_number': invoice_number,
                'ordered_items': ordered_items,
                'payment_method': payment_method,
                'total_amount': total_amount,
                'grand_total': grand_total,
            }
            return render(request, 'app/invoice.html', context)
    else:
        return render(request, 'app/invoice.html')

#for pdf
def download_pdf(request):
    user = request.user
    customer = Customer.objects.filter(user=user).first()
    latest_order = OrderPlaced.objects.filter(user=user).order_by('-id').first()
    if latest_order:
        selected_address = latest_order.customer
        today = datetime.date.today()
        latest_invoice = OrderPlaced.objects.latest('id')
        invoice_number = latest_invoice.id + 100
        ordered_item = latest_order.product
        if latest_order.payment:
            payment_method = latest_order.payment.payment_method
        else:
            payment_method = "Cash on Delivery"
        total_amount = latest_order.total_cost
        last_payment = Payment.objects.filter(user=user, paid=True).order_by('-id').first()
        if last_payment:
            grand_total = total_amount + 60
        else:
            grand_total = 0
        # Prepare data for each ordered item
        item_data = {
            'title': ordered_item.title,
            'category': ordered_item.category,
            'quantity': latest_order.quantity,
            'final_price': ordered_item.discounted_price * latest_order.quantity
        }
        context = {
            'user': user,
            'customer': customer,
            'selected_address': selected_address,
            'today': today,
            'invoice_number': invoice_number,
            'ordered_items': [item_data],
            'payment_method': payment_method,
            'total_amount': total_amount,
            'grand_total': grand_total,
        }
        return invoice_generator(request, latest_order, selected_address, today, invoice_number, payment_method, total_amount, grand_total)
    else:
        return HttpResponse("No orders found to generate invoice.")
    
def invoice_generator(request, order, selected_address, today, invoice_number, payment_method, total_amount, grand_total):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    elements = []
    
    styles = getSampleStyleSheet()
    center_style = styles["Normal"]
    center_style.alignment = 1
    invoice_title_style = styles['Title'].clone('InvoiceTitle')
    invoice_title_style.fontSize = 18
    invoice_title_style.textColor = colors.blue
    
    # Add invoice header
    invoice_header = Paragraph('<b>BOOKIFY Live</b><br/>Online Book Store<br/>Customer Care : 1800-725-4207', center_style)
    elements.append(invoice_header)

    # Add divider
    elements.append(Spacer(1, 20))
    divider = Paragraph('<u>_____________________________________________________________________________________________</u>', center_style)
    elements.append(divider)

    # Add bill details
    bill_details = [
        f'<div style="text-align: left;">'
        f'<b>Bill To:</b> {request.user.username.upper()}<br/>',
        f'<b>Date:</b> {today}<br/>',
        f'<b>Invoice Number:</b> {invoice_number}<br/>',
        f'</div>',
        f'<div style="text-align: right;">'
        f'<b>Ship To:</b><br/>{selected_address.name.upper()}<br/>{selected_address.locality}<br/>{selected_address.state}, PIN {selected_address.zipcode}<br/>Mobile: {selected_address.mobile}'
        f'</div>'
    ]

    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph('<b>INVOICE</b>', invoice_title_style))

    elements.append(Spacer(1, 0.5 * inch))
    
    for detail in bill_details:
        elements.append(Paragraph(detail))

    elements.append(Spacer(1, 0.5 * inch))

    # Add ordered items table
    table_data = [["Item", "Category", "Qty", "Payment Method"]]
    for order_item in OrderPlaced.objects.filter(id=order.id).select_related('product'):
        table_data.append([order_item.product.title, order_item.product.category, order_item.quantity, payment_method])
    table = Table(table_data, colWidths=[200, 100, 50, 150])
    
    # Style the table
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5), 
    ])
    table.setStyle(table_style)

    elements.append(table)
    elements.append(Spacer(1, 0.5 * inch))
    
    # Add total amount and grand total
    total_data = [
        ["Total Amount", f'Rs. {total_amount}'],
        ["Shipping", "Rs. 40.00"],
        ["Tax", "Rs. 20.00"],
        ["Offer", "0.00"],
        ["Grand Total", f'Rs. {grand_total}']
    ]

    second_table = Table(total_data, colWidths=[2 * inch, 2 * inch])

    second_table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.red),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ])
    second_table.setStyle(second_table_style)
    elements.append(second_table)

    # Add thank you message
    elements.append(Spacer(1, 20))
    elements.append(Paragraph('<b>THANK YOU FOR SHOPPING</b>', styles['Normal']))

    # Build the PDF
    doc.build(elements)
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename=f'Invoice_{invoice_number}.pdf')
    
@login_required
def orders(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user).order_by('-ordered_date')
    paginator = Paginator(order_placed, 5)
    page_number = request.GET.get('page')
    try:
        order_placed = paginator.page(page_number)
    except PageNotAnInteger:
        order_placed = paginator.page(1)
    except EmptyPage:
        order_placed = paginator.page(paginator.num_pages)
    try:
        wallet = Wallet.objects.get(user=request.user)
        wallet_transactions = Payment.objects.filter(user=request.user, payment_method='Wallet')
    except Wallet.DoesNotExist:
        wallet = Wallet.objects.create(user=request.user, balance=0)
        wallet_transactions = []
    return render(request,'app/orders.html', {'order_placed': order_placed, 'wallet': wallet, 'wallet_transactions': wallet_transactions, 'page_number': page_number})

@login_required
@transaction.atomic
def cancel_order(request, order_id):
    order = get_object_or_404(OrderPlaced, id=order_id, user=request.user)
    if order.status not in ['Delivered', 'On the way']:
        if order.payment and order.payment.payment_method == 'Wallet':
            wallet = Wallet.objects.get(user=request.user)
            wallet.balance += order.payment.amount
            wallet.save()
            WalletTransaction.objects.create(
                user=request.user,
                type='REFUND',
                amount=order.payment.amount
            )
            messages.success(request, "Your order has been cancelled and refunded to your wallet.")
        order.status = 'Cancelled'
        order.save()
        if order.payment and order.payment.payment_method == 'Razorpay': # Check if payment exists
            if not order.payment.refunded:
                wallet = Wallet.objects.get(user=request.user)
                wallet.balance += order.payment.amount
                wallet.save()
                order.payment.refunded = True
                order.payment.save()
                messages.success(request, "Your online order has been cancelled and refunded to your wallet.")
                # Create a wallet transaction record for the refund
                WalletTransaction.objects.create(
                    user=request.user,
                    type='REFUND',
                    amount=order.payment.amount
                )
            else:
                messages.error(request, "Your order has already been refunded.")
        else:
            # Handle cash on delivery orders (no payment object)
            messages.success(request, "Your order has been cancelled.")
    else:
        messages.error(request, "Your order cannot be cancelled at this stage.")
    return redirect('orders')

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(OrderPlaced, id=order_id, user=request.user)
    if order.status == "Cancelled" or order.status == "Return Approved":
        order.delete()
        #messages.success(request, "Cancelled Order deleted successfully!")
    else:
        messages.error(request, "Cannot delete order. It is not cancelled.")
    return redirect("orders")

@login_required
def return_order(request, order_id):
    order = OrderPlaced.objects.get(id=order_id)
    if request.method == 'POST':
        reason = request.POST.get('reason')
        if reason:
            print("Reason for return:", reason)
            order.status = 'Return Requested'
            order.return_reason = reason # Save the return reason
            order.save()
            return redirect('orders')
    context = {
        'order': order,
    }
    return render(request, 'app/return_order.html', context)

@login_required
def cancel_return(request, order_id):
    order = get_object_or_404(OrderPlaced, id=order_id)
    if order.status == 'Return Requested':
        order.status = 'Delivered'  # Or whatever status you want to set
        order.save()
    return redirect('orders')

@login_required
def wallet(request):
    transactions = WalletTransaction.objects.filter(user=request.user).order_by('-date')
    wallet_balance = Wallet.objects.get(user=request.user).balance
    paginator = Paginator(transactions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'app/wallet.html', {'page_obj': page_obj, 'wallet_balance': wallet_balance})

#add to wallet section
# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
@login_required
def add_to_wallet(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount')) * 100  # Convert amount to paisa
        # Generate Razorpay order for the specified amount
        order_data = {
            'amount': amount,
            'currency': 'INR',
            'payment_capture': '1'  # Auto-capture payment after successful transaction
        }
        order = client.order.create(data=order_data)
        order_id = order['id']
        return redirect('wallet')
    return redirect('wallet')

def create_razorpay_order(request):
    amount = int(request.POST.get('amount', 0))
    if amount > 0:
        # Create a Razorpay order and return its details
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        razor_amount = amount * 100  # Amount should be in paise
        data = {
            "amount": razor_amount,
            "currency": "INR"
            # You can add more options if required
        }
        order = client.order.create(data=data)
        return JsonResponse({'id': order['id'], 'amount': order['amount']})
    else:
        return JsonResponse({'error': 'Invalid amount'}, status=400)

@login_required
def process_payment(request):
    order_id = request.GET.get('order_id')
    amount = request.GET.get('amount')
    return render(request, 'app/wallpay.html', {'order_id': order_id, 'amount': amount})

    
def hrishi(request):
    return render(request, 'app/hrishi.html')

@login_required
def plus_wishlist(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user,product=product).save()
        data={
            'message':'Wishlist added successfully',
        }
        return JsonResponse(data)

@login_required 
def minus_wishlist(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user,product=product).delete()
        data={
            'message':'Wishlist removed successfully',
        }
        return JsonResponse(data)  

@login_required
def show_wishlist(request):
    user = request.user
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Wishlist.objects.filter(user=user)
    return render(request,'app/wishlist.html',locals())

@login_required
def delete_from_wishlist(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    # Get the wishlist item and delete it
    wishlist_item = Wishlist.objects.filter(user=user, product=product)
    if wishlist_item.exists():
        wishlist_item.delete()
        messages.success(request, "Item removed from wishlist successfully!")
    else:
        messages.error(request, "Item does not exist in the wishlist.")
    return redirect("showwishlist")

#otp verification
def generate_otp(size=6):
    """Generate a 6-digit OTP"""
    numbers = '0123456789'
    otp = ''.join(random.choice(numbers) for _ in range(size))
    return otp
def send_otp_email(email, otp):
    subject = 'Complete Your Sign Up'
    context = {
        'otp': otp,
        'brand_name': 'BOOKIFY live',  # You can customize this
        # Add any other context variables you might need in your email template
    }
    html_message = render_to_string('app/email_templates/otp_email.html', context)
    plain_message = strip_tags(html_message)  # Fallback for email clients that do not support HTML
    from_email = 'vishnusreqourse@gmail.com'
    to = email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message, fail_silently=False)
User = get_user_model()

def subscribe(request):
    form = SubscribeForm()
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            users = User.objects.filter(email=email)
            
            if users.exists():
                otp = generate_otp()
                # Iterate through all users with the given email and update/create Customer
                for user in users:
                    # Use first() instead of get() to handle MultipleObjectsReturned
                    customer = Customer.objects.filter(user=user).first()
                    if customer:
                        customer.otp = otp
                        customer.save()
                    else:
                        # Create a new Customer if not exists
                        customer = Customer.objects.create(user=user, otp=otp)
                # Since all relevant users share the same email, send one OTP
                send_otp_email(email, otp)
                messages.success(request, 'An OTP has been sent to the shared email.')
                # Store the email in the session
                request.session['recipient_email'] = email
                # Redirect to OTP verification page, might need adjustments to handle multiple users
                return redirect('otp_verification')
            else:
                # No user found with that email
                messages.error(request, 'No account found with the provided email.')
    return render(request, 'app/emailotp.html', {'form': form})

# New view for OTP verification
def otp_verification(request):
    email = request.session.get('recipient_email', None)
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        print("OTP Entered:", otp_entered)  # Debugging
        try:
            # Use filter() instead of get() due to multiple users having the same email
            users = User.objects.filter(email=email)
            if not users:
                raise User.DoesNotExist
            
            customer = None
            for user in users:
                try:
                    customer = Customer.objects.get(user=user, otp=otp_entered)
                    break  # Break the loop if the correct customer is found
                except Customer.DoesNotExist:
                    continue  # Try the next user if no matching customer is found
            
            if customer is None:
                raise Customer.DoesNotExist

            print("Customer Found:", customer.user.username)  # Debugging

            # Clear the OTP after successful verification if needed
            customer.otp = None
            customer.save()

            # OTP verified successfully
            messages.success(request, 'OTP verified successfully.')
            return redirect('login')  # Ensure you have a URL named 'login'
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email.')
        except Customer.DoesNotExist:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'app/otp_signup.html', {'email': email})

#advanced search
@property
def popularity(self):
    return OrderPlaced.objects.filter(product=self).count()

@login_required
def search_results(request):
    query = request.GET.get('query', '')
    sort_by = request.GET.get('sort_by', None)

    # Basic search functionality
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    # Simplified Sorting logic
    if sort_by == 'price_asc':
        products = products.order_by('selling_price')
    elif sort_by == 'price_desc':
        products = products.order_by('-selling_price')
    elif sort_by == 'a_z':
        products = products.order_by('title')
    elif sort_by == 'z_a':
        products = products.order_by('-title')
    elif sort_by == 'new_arrivals':
        products = Product.objects.order_by('-id')[:10]
    
    # Get the top selling products
    top_selling_products = Product.objects.annotate(num_orders=Count('orderplaced')).order_by('-num_orders')[:10]
    #pagination
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))

    context = {
        'page_obj': page_obj,
        'products': products,
        'query': query,
        'sort_by': sort_by,
        'top_selling_products': top_selling_products,
        'totalitem': totalitem,
        'wishitem': wishitem,
    }
    return render(request, 'app/search_results.html', context)


#########################################################################
#########################################################################
#for twilio
# def register(request):
#     if request.method == "POST":
#         if User.objects.filter(username__iexact=request.POST['user_name']).exists():
#             return HttpResponse("User already exists")

#         user = User.objects.create(username=request.POST['user_name'])
#         otp = random.randint(1000, 9999)
#         customer = Customer.objects.create(user=user, phone_number=request.POST['phone_number'], otp=f'{otp}')
       
#         message_handler = MessageHandler(request.POST['phone_number'], otp)
#         message_handler.send_otp_via_message()

#         red = redirect(f'otp/{customer.uid}/')
#         red.set_cookie("can_otp_enter", True, max_age=600)
#         return red

#     return render(request, 'registration.html')

# def otpVerify(request,uid):
#     if request.method=="POST":
#         profile=Profile.objects.get(uid=uid)     
#         if request.COOKIES.get('can_otp_enter')!=None:
#             if(profile.otp==request.POST['otp']):
#                 red=redirect("profile")
#                 red.set_cookie('verified',True)
#                 return red
#             return HttpResponse("wrong otp")
#         return HttpResponse("10 minutes passed")        
#     return render(request,"otp.html",{'id':uid})
#end of twilio logics
#admin panel
# def adminLogin(request):
#     return render(request,"app/admin/signin.html")

# @login_required(login_url="/admin/")
# def admin_home(request):
#     return render(request,"admin/admin_home.html")

# def adminLoginProcess(request):
#     username=request.POST.get("username")
#     password=request.POST.get("password")

#     user=authenticate(request=request,username=username,password=password)
#     if user is not None:
#         login(request=request,user=user)
#         return HttpResponseRedirect(reverse("admin_home"))
#     else:
#         messages.error(request,"Error in Login! Invalid Login Details!")
#         return HttpResponseRedirect(reverse("admin_login"))