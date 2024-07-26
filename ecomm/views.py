from django.shortcuts import get_object_or_404, render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.utils import timezone
from django.db.models import Sum, Count
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.storage import FileSystemStorage


from ecomm.models import category,Product,Cart,Slide,CartItem,Order,OrderItem,Review


# Create your views here.
def home(request):
    slides = Slide.objects.all()  # Fetch all slider images
    products = Product.objects.all()  # Fetch all products
    categories = category.objects.all()  # Fetch all categories
    
    products = Product.objects.all()
    context={'products': products,'slides': slides,'categories': categories}
    return render(request, 'index.html',context )
    

def login1(request):
    if request.method=="POST":
        username=request.POST.get("username")
        pass1=request.POST.get("password")
        user=authenticate(request,username=username,password=pass1)
        if user and user.is_superuser:
            login(request,user)
            return redirect("dashboard")
        elif user is not None:
            login(request,user)
            return redirect("home")
        else:
            return HttpResponse("Invalid Username or Password")
    return render(request, 'login.html')

def signup(request):
    if request.method=="POST":
        name=request.POST.get("username")
        email=request.POST.get("email")
        address=request.POST.get("address")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        if password1!=password2:
            return HttpResponse("Password Does Not Match")
        my_user=User.objects.create_user(name,email,password1)
        my_user.save()
        return redirect("login1")
        
    return render(request, 'signup.html')

def admin1(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user_obj=User.objects.filter(username=username)
        if not user_obj.exists():
            messages.info(request,"ACCOUNT NOT FOUND")
        user_obj=authenticate(username=username,password=password)
        if user_obj and user_obj.is_superuser:
            login(request,user_obj)
            return redirect("dashboard")
        messages.info(request,"INVALID PASSWORD")
        return redirect("home")
    
    return render(request,"admin.html")

def contact_us(request):
    return render(request,"contact_us.html")


def dashboard(request):
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    total_categories = category.objects.count()
    total_products = Product.objects.count()
    total_sales = Order.objects.aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
    total_dynamic_sliders=Slide.objects.count()

    context = {
        'total_orders': total_orders,
        'total_users': total_users,
        'total_categories': total_categories,
        'total_products': total_products,
        'total_sales': total_sales,
        'total_dynamic_sliders':total_dynamic_sliders,
    }

    return render(request, 'dashboard.html', context)
    

def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category')  

      
        if not category_name:
            return HttpResponse("Category name cannot be empty.")

 
        new_category = category(name=category_name)
        new_category.save()
        messages.info(request,"CATEGORY ADDED SUCCESSFULLY")

      
        return redirect('dashboard')  


 
        
    return render(request,"add_category.html")


def list_category(request):
    categories=category.objects.all()
    context={
        "categories":categories
    }
    return render(request,"list_category.html",context)


def add_product(request):
    
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')  

        cat = category.objects.get(id=category_id)
        product = Product(name=name, description=description, price=price, category=cat, image=image)
        product.save()
        return redirect('list_product')
    
    categories = category.objects.all()
    context={
        "categories": categories
    }
    return render(request, "add_product.html", context)


def list_product(request):
    products=Product.objects.all()
    context={
        "products":products
    }
    return render(request,"list_product.html",context)


def user_logout(request):
    logout(request)
    return redirect('home') 

def edit_category(request,pk):
    categories=get_object_or_404(category,pk=pk)
    if request.method=="POST":
        categories.name=request.POST.get('name')
        categories.save()
        return redirect("list_category")
    context={
        "categories":categories
    }
    return render(request,"update_category.html",context)

def delete_category(request,pk):
    categories=get_object_or_404(category,pk=pk)
    if request.method=="POST":
        categories.delete()
        return redirect("list_category")
    context={"categories": categories}
    return render(request,"delete_category.html",context)


def update_product(request,pk):
    product = get_object_or_404(Product,pk=pk)
    categories = category.objects.all()
    if request.method == 'POST':
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.category_id = request.POST['category']
        product.save()
        return redirect('list_product')
    context={"product": product,
             "categories":categories
             }
    return render(request, "update_product.html", context)


def delete_product(request,pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('list_product') 
    context={"product": product}
    return render(request, 'delete_product.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')
@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    context={'cart_items': cart_items}
    return render(request, 'cart_detail.html', context)



def upload_slider(request):
    

  if request.method == 'POST' and request.FILES.get('slider_file'):
        slider_file = request.FILES['slider_file']
        slider_title = request.POST.get('slider_title')

        # Create a new Slide object
        Slide.objects.create(slider_file=slider_file, slider_title=slider_title)

        return redirect('upload_slider') 
  return render(request, 'upload_slider.html')

@login_required
def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart_detail')  # Redirect back to the cart detail page
from django.http import JsonResponse

@login_required
def update_cart_item(request, item_id):
    if request.method == "POST":
        quantity = request.POST.get("quantity")
        cart_item = get_object_or_404(CartItem, id=item_id)
        if quantity.isdigit() and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
            return JsonResponse({"success": True})
    return JsonResponse({"success": False})

def checkout(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        if not all([name, email, phone, address, payment_method]):
            messages.error(request, "Please fill out all fields.")
            return redirect('checkout')

        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        # Create an order
        order = Order.objects.create(
            user=request.user,
            name=name,
            email=email,
            phone=phone,
            address=address,
            payment_method=payment_method,
            total_amount=sum(item.product.price * item.quantity for item in cart_items)
        )

        # Save order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear the cart
        cart_items.delete()

        
        return redirect('payment_success',order_id=order.id)

    return render(request, 'checkout.html')

def payment_success(request, order_id):
    order = get_object_or_404(Order,id=order_id)
    context = {
        'order': order,
        'order_items': order.items.all(),
    }
    return render(request, 'payment_success.html', context)


def view_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    print(orders)
   
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    context={
        "orders":orders,
        "cart":cart,
        "cart_items":cart_items
    }
    return render(request,"view_order.html",context)


def delete_order(request,order_id):
    order=get_object_or_404(Order, id=order_id, user=request.user)
    order.delete()
    return redirect('view_orders')


def category_list(request):
    categories = category.objects.all()
    context={'categories': categories}
    return render(request, 'category_list.html',context )

def category_detail(request, cat_id):
    category_obj = get_object_or_404(category, id=cat_id)
    products = Product.objects.filter(category=category_obj)
    context = {'category': category_obj, 'products': products}
    return render(request, 'category_detail.html', context)

@staff_member_required
def view_analytics(request):
    
    end_date = timezone.now()
    start_date = end_date - timezone.timedelta(days=30)

    
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    if start_date_str and end_date_str:
        start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d')

    total_orders = Order.objects.filter(created_at__range=(start_date, end_date)).count()
    total_users = User.objects.filter(date_joined__range=(start_date, end_date)).count()
    total_categories = category.objects.count()  
    total_products = Product.objects.filter(created_at__range=(start_date, end_date)).count()
    total_sales = Order.objects.filter(created_at__range=(start_date, end_date)).aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0

    context = {
        'total_orders': total_orders,
        'total_users': total_users,
        'total_categories': total_categories,
        'total_products': total_products,
        'total_sales': total_sales,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
    }

    return render(request, 'view_analytics.html', context)


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    for order in orders:
        order.total_price = sum(item.quantity * item.price for item in order.items.all())
    
    context= {'orders': orders}
    return render(request, 'order_history.html',context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review')
        
        if rating and review_text:
            Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                review=review_text
            )
    
    context = {
        'product': product,
        'reviews': reviews
    }
    return render(request, 'product_detail.html', context)


def download_receipt(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{order_id}.pdf"'
   
    return response

def add_feedback(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        # Save feedback to the database
        return redirect('payment_success', order_id=order.id)
    return render(request, 'add_feedback.html', {'order': order})
        

def submit_review(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        rating = request.POST.get('rating')
        review_text = request.POST.get('review')
        
        # Save the review
        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            review=review_text
        )
        
        return redirect('product_detail', product_id=product_id)  # Redirect to the product detail page
    else:
        return render(request,'error.html', {'error': 'Invalid request method'})
    

    # return HttpResponse(status=405) 

    