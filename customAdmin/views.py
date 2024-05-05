from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from app.models import Coupon, Product, CATEGORY_CHOICES, Category, OrderPlaced, ProductOffer, Wallet, OrderPlaced, WalletTransaction
from app.forms import CouponForm, EditOrderForm, ProductForm, EditProductForm, ProductIdForm,CustomerRegistrationForm,CategoryForm,EditUserForm,OrderStatusForm, ProductOfferForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import date, timedelta, datetime
from django.utils.translation import gettext as _
#Generate PDF report
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Image
from django.utils import timezone
from django.views.decorators.cache import never_cache
#diagram
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.core.paginator import Paginator
# Create your views here.
def admin_login(request):
    try:
        if request.user.is_authenticated:
            return redirect('dashboard')
        #messages.info(request,'Account not found)
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username = username)
            if not user_obj.exists():
                messages.info(request,'Account not found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            user_obj = authenticate(username=username,password=password)

            if user_obj and user_obj.is_superuser:
                login(request,user_obj)
                return render(request,'admin_home.html')
            
            messages.info(request,'Invalid password')
            return redirect('/')
        return render(request,'adminlogin.html')
    
    except Exception as e:
        print(e)
        # return render(request, 'adminlogin.html')

@login_required
@never_cache
def admin_logout(request):
    logout(request)
    return redirect('/admin/')

@login_required
def dashboard(request):
    return render(request,'dashboard.html')

@login_required
def admin_home(request):
    return render(request,'admin_home.html')

@login_required
def adminprofile(request):
    return render(request,'adminprofile.html')

@login_required
def all_products(request):
    products=Product.objects.all()
    return render(request,'all_products.html',{'products': products})

@login_required
def add_products(request):
        if request.method=='POST':
            form = ProductForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                return redirect('all_products')
            else:
                messages.error(request, "Please fill in all required fields.")
        else:
            form=ProductForm()
        return render(request, 'add_products.html', {'form': form})

@login_required
def edit_products(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('all_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_products.html', {'form': form})

@login_required
def manage_products(request):
    products = Product.objects.all()
    paginator = Paginator(products, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'manage_products.html',{'page_obj': page_obj})

@login_required
def delete_product(request, pk):
    # Optional: Add permission check here to ensure only authorized users can delete
    if request.user.is_superuser:
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return redirect(reverse('manage_products'))
    else:
        return redirect(reverse('admin_login'))

@login_required
def all_users(request):
    users = User.objects.all().order_by('-id')
    return render(request, 'all_users.html', {'users': users})

@login_required
def add_users(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # This saves the new User object
            return redirect('all_users')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'add_users.html', {'form': form})

@login_required
def edit_users(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = EditUserForm(instance=user)
    return render(request, 'edit_users.html', {'form': form, 'user': user})

@login_required
def manage_users(request):
    users = User.objects.all().order_by('-id')
    paginator = Paginator(users, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'manage_users.html', {'page_obj': page_obj})

@login_required
def delete_user(request, pk):
    # Make sure only superusers or staff can delete users, or implement your own permission checks
    if request.user.is_superuser:
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return redirect(reverse('manage_users'))
    else:
        return redirect(reverse('admin_login'))
    
@login_required
def block_user(request, pk):
    if request.user.is_superuser:
        user = User.objects.get(pk=pk)
        user.is_active = False
        user.save()
        return redirect('manage_users')
    return redirect('/')  # Or appropriate access denied response

@login_required
def unblock_user(request, pk):
    if request.user.is_superuser:
        user = User.objects.get(pk=pk)
        user.is_active = True
        user.save()
        return redirect('manage_users')
    return redirect('/')

@login_required
def all_categories(request):
    # Pass CATEGORY_CHOICES directly to the template context
    return render(request, 'all_categories.html', {'categories': CATEGORY_CHOICES})

@login_required
def add_categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_categories')
    else:
        form = CategoryForm()
    categories = Category.objects.all()  # Get all categories to display
    return render(request, 'add_categories.html', {'form': form, 'categories': categories})

@login_required
def edit_categories(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('add_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_categories.html', {'form': form})

@login_required
def delete_category(request, pk):
    category = Category.objects.get(pk=pk)
    category.delete()
    return redirect(reverse('add_categories'))

#order management
@login_required
def list_orders(request):
    orders = OrderPlaced.objects.all().order_by('-ordered_date')  # Fetch all orders
    paginator = Paginator(orders, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}  # Pass the paginated queryset to the template context
    return render(request, 'list_orders.html', context)

@login_required
def manage_orders(request):
    orders = OrderPlaced.objects.all().order_by('-ordered_date')
    paginator = Paginator(orders, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'manage_orders.html', {'page_obj': page_obj})

@login_required
def edit_order(request, pk):
    order = get_object_or_404(OrderPlaced, pk=pk)
    if order.status == 'Cancelled':
        messages.error(request, "This order has already been cancelled by the user.")
        return redirect(reverse('manage_orders'))
    if request.method == 'POST':
        form = EditOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('manage_orders')
    else:
        form = EditOrderForm(instance=order)
    return render(request, 'edit_order.html', {'form': form, 'order': order})
    
@login_required
def cancel_order(request, pk):
    # Ensure only superusers or staff can cancel orders
    if request.user.is_superuser:
        order = get_object_or_404(OrderPlaced, pk=pk)
        # Assuming 'Cancelled' is a valid status in your OrderPlaced model's status field choices
        order.status = 'Cancelled'
        order.save()
        return redirect(reverse('manage_orders'))
    else:
        # Redirect to a login page or deny access if the user does not have superuser status
        return redirect(reverse('manage_orders'))
    
@login_required
def return_requests(request):
    return_orders = OrderPlaced.objects.filter(status='Return Requested')
    return render(request, 'return_request.html', {'return_orders': return_orders})

@login_required
def admin_approval(request, order_id):
    order = get_object_or_404(OrderPlaced, id=order_id)
    # Check if the order has a payment
    if order.payment:
        # If payment exists, update wallet balance and mark payment as refunded
        wallet, created = Wallet.objects.get_or_create(user=order.user)
        wallet.balance += order.total_cost
        wallet.save()
        order.payment.refunded = True
        order.payment.save()
    else:
        wallet, created = Wallet.objects.get_or_create(user=order.user)
        wallet.balance += order.total_cost
        wallet.save()
    WalletTransaction.objects.create(
        user=order.user,
        type='RETURN-REFUND',
        amount=order.total_cost
    )  
    # Update order status
    order.status = 'Return Approved'
    order.save()
    return redirect('return-requests')

#coupon management
@login_required
def all_coupons(request):
    coupons = Coupon.objects.all()
    return render(request, 'all_coupons.html', {'coupons': coupons})

@login_required
def add_coupons(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_coupons')
    else:
        form = CouponForm()
    coupons = Coupon.objects.all()  # Get all coupons to display
    return render(request, 'add_coupons.html', {'form': form, 'coupons': coupons})

@login_required
def edit_coupons(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect('add_coupons')
    else:
        form = CouponForm(instance=coupon)
    return render(request, 'edit_coupon.html', {'form': form})

@login_required
def delete_coupon(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    coupon.delete()
    return redirect(reverse('add_coupons'))

@login_required
def list_product_offers(request):
    product_offers = ProductOffer.objects.all()
    return render(request, 'all_offers.html', {'product_offers': product_offers})

@login_required
def add_product_offer(request):
    if request.method == 'POST':
        form = ProductOfferForm(request.POST)
        if form.is_valid():
            form.save()
            product_offers = ProductOffer.objects.all()
            return render(request, 'edit_offers.html', {'form': form, 'product_offers': product_offers})
    else:
        form = ProductOfferForm()
        product_offers = ProductOffer.objects.all()  # Add this line to create an empty product_offer object
    return render(request, 'edit_offers.html', {'form': form, 'product_offers': product_offers})

@login_required
def delete_product_offer(request, pk):
    product_offer = get_object_or_404(ProductOffer, pk=pk)
    product_offer.delete()
    product_offers = ProductOffer.objects.all()
    return redirect('add_product_offer')

# Sales Report Area
@login_required
def report_generator(request, orders, from_date, to_date):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    story = []
    
    # Get sample styles
    styles = getSampleStyleSheet()
    styles['Heading1'].alignment = 1
    styles['Heading3'].alignment = 1
    styles['Heading4'].alignment = 1

    # Add Bookify Live h1 title
    bookify_title = '<h1 style="text-align:center; text-shadow: 0 0 5px #00ff00, 0 0 10px #00ff00, 0 0 15px #00ff00, 0 0 20px #00ff00, 0 0 25px #00ff00, 0 0 30px #00ff00, 0 0 35px #00ff00;">BOOKIFY</h1>'
    story.append(Paragraph(bookify_title, styles["Heading1"]))

    # Add Sales report h3 title
    sales_title = '<h3 style="text-align:center; margin-bottom: 5px;">Sales report</h3>'
    story.append(Paragraph(sales_title, styles["Heading3"]))

    # Add printed timestamp h4 title
    printed_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    printed_title = f'<h4 style="text-align:center; margin-top: 5px;">Printed on {printed_time}</h4>'
    story.append(Paragraph(printed_title, styles["Heading4"]))

    # Add some space between titles
    story.append(Spacer(1, 20))

    data = [["Order ID", "Quantity", "Product ID", "Product Name", "Amount"]]
    for order in orders:
        # Retrieve order items associated with the current order
        order_items = OrderPlaced.objects.filter(id=order.id)
        total_quantity = sum(item.quantity for item in order_items)

        if order_items.exists():
            product_id = ", ".join([str(item.product.id) for item in order_items])
            product_name = ", ".join([str(item.product.title) for item in order_items])
            total_amount = sum(item.product.discounted_price * item.quantity for item in order_items)
        else:
            product_ids = "N/A"
            product_names = "N/A"
            total_amount = 0

        data.append([order.id, total_quantity, product_id, product_name, total_amount])
    # Create a table with the data
    table = Table(data, colWidths=[1 * inch, 1.5 * inch, 2 * inch, 3 * inch, 1 * inch])
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

    # Add the table to the story
    story.append(table)

    # Add space between tables
    story.append(Spacer(1, 0.5 * inch))

    #total_discounts = sum(1 for order in orders if order.discount_applied)
    #total_coupons_deducted = sum(1 for order in orders if order.coupon_applied)
    number_of_days_selected = (to_date - from_date).days + 1
    total_sales_count = len(orders)
    total_order_amount = sum(order.total_cost for order in orders)
    total_quantities_sold = sum(order.quantity for order in orders)

    # Define the data for the new table
    additional_data = [
        ["Grant totals", "counts"],
        ["Number of days", number_of_days_selected],
        ["Total quantity sold", total_quantities_sold],
        #["Total Discounts", total_discounts],
        #["Total Coupons Deducted", total_coupons_deducted],
        ["Total Sales", total_sales_count],
        ["Total Order Amount", total_order_amount],
    ]

    additional_table = Table(additional_data, colWidths=[2 * inch, 2 * inch])

    additional_table_style = TableStyle([
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
    additional_table.setStyle(additional_table_style)
    story.append(additional_table)

    # Build the document
    doc.build(story)
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='Bookify_salesreport.pdf')

def report_pdf_order(request):
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        time_period = request.POST.get('time_period')

        if not from_date or not to_date:
            return HttpResponse('Please select both from date and to date.')

        try:
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponse('Invalid date format.')
        
        if time_period:
            if time_period == '1_day':
                to_date = datetime.now().date()
                from_date = to_date - timedelta(days=1)
            elif time_period == '1_week':
                to_date = datetime.now().date()
                from_date = to_date - timedelta(weeks=1)
            elif time_period == '1_month':
                to_date = datetime.now().date()
                from_date = to_date - timedelta(days=30)  # Approximating 1 month as 30 days
            else:
                # Handle invalid time period
                return HttpResponse('Invalid time period selected.')

        orders = OrderPlaced.objects.filter(ordered_date__range=[from_date, to_date]).order_by('-id')
        return report_generator(request, orders, from_date, to_date)

#othersss   
@login_required
def sales_calculation(start_date, end_date):
    if start_date == end_date:
        date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        order_items = OrderPlaced.objects.filter(order__created_at__date=date_obj)
    else:
        order_items = OrderPlaced.objects.filter(order__created_at__gte=start_date, order__created_at__lte=end_date)

    if order_items:
        order_count = order_items.distinct('order').count()
        order_item_count = order_items.count()

        delivered_items = order_items.filter(status__iexact="Delivered")
        delivered_items_count = delivered_items.count()

        product_price_sum = sum(item.product_price * item.quantity for item in delivered_items)

        raz_total = sum(item.product_price * item.quantity for item in delivered_items.filter(order__payment__payment_method__method="raz_method"))
        
        cod_total = sum(item.product_price * item.quantity for item in delivered_items.filter(order__payment__payment_method__method="cod_method"))

        calculation = {
            'delivered_items_count': delivered_items_count,
            'order_item_count': order_item_count,
            'product_price_sum': product_price_sum,
            'order_count': order_count,
            'raz_total': raz_total,
            'cod_total': cod_total,
        }
        return calculation
    else:
        return {}

@login_required
def sales_report(request):
    if not request.user.is_superuser:
        messages.error(request, _('Only admin can access this page!'))
        return redirect('admin_login')

    context = {}
    s_date = None
    e_date = None
    start_date = None
    end_date = None

    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        if start_date == "":
            messages.error(request, _('Start date not entered'))
            return redirect('sales_report')
        if end_date == "":
            messages.error(request, _('End date not entered'))
            return redirect('sales_report')

        if start_date == end_date:
            messages.warning(request, _('Please select a start date and end date must be different!'))
            return redirect('sales_report')

        order_items = OrderPlaced.objects.filter(order__created_at__gte=start_date, order__created_at__lte=end_date)

        if order_items:
            context.update(sales=order_items, s_date=start_date, e_date=end_date)
            context.update(sales_calculation(start_date=start_date, end_date=end_date))
            messages.success(request, _('Here is the sales report covering the period from {start_date} to {end_date}.'))
        else:
            messages.error(request, _('No data found at the specific date!'))

    return render(request, 'sales.html', context)

#sales diagram
@login_required
def bardiagram(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # Filter orders based on the selected date range
        orders = OrderPlaced.objects.filter(ordered_date__range=[start_date, end_date])
    else:
        # If no date range is selected, fetch all orders
        orders = OrderPlaced.objects.all()
    
    # Retrieve sales data
    order_dates = [order.ordered_date.date() for order in orders]

    # Count the number of orders per day
    from collections import Counter
    order_count_by_day = Counter(order_dates)

    # Prepare data for the bar diagram
    dates = list(order_count_by_day.keys())
    order_counts = list(order_count_by_day.values())

    # Create the bar diagram
    plt.figure(figsize=(10, 6))
    plt.bar(dates, order_counts, color='green')
    plt.xlabel('Date')
    plt.ylabel('Number of Orders')
    plt.title('Daily Sales Report')
    plt.xticks(rotation=0)
    plt.tight_layout()

    # Save the diagram to a BytesIO buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode the buffer to base64
    diagram_data = base64.b64encode(buffer.getvalue()).decode()

    # Render the template with the diagram data
    return render(request, 'diagramview.html', {'diagram_data': diagram_data})
