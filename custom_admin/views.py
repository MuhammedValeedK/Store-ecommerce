from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from ecommerceapp.models import Product, Orders
from ecommerceapp.models import Orders  
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from ecommerceapp.forms import ProductForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseNotFound
from ecommerceapp.models import Category 
from ecommerceapp.forms import CategoryForm


@never_cache
@login_required
@staff_member_required
def dashboard_view(request):
    User = get_user_model()
    total_users = User.objects.count()  # Total users
    total_products = Product.objects.count()  # Total products
    total_orders = Orders.objects.count()  # Total orders
    
    return render(request, 'custom_admin/dashboard.html', {
        'title': 'Admin Dashboard',
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
    })








@never_cache
@login_required
@staff_member_required
def manage_orders_view(request):
    orders = Orders.objects.all()
    return render(request, 'custom_admin/manage_orders.html', {
        'orders': orders,
    })




@never_cache
@login_required
@staff_member_required
def create_user_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        # Basic validation
        if not username or not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return redirect('custom_admin:create_user')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('custom_admin:create_user')

        # Check if the username or email is already in use
        User = get_user_model()
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Username or Email already exists.")
            return redirect('custom_admin:create_user')

        # Create the user
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "User created successfully!")
        return redirect('custom_admin:manage_users')

    return render(request, 'custom_admin/create_user.html')

User = get_user_model()
@login_required
@user_passes_test(lambda u: u.is_staff)
def list_users_view(request):
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )
    else:
        users = User.objects.all()
    return render(request, 'custom_admin/list_users.html', {'users': users})



# Ensure only staff members can access these views
@never_cache
@login_required
@user_passes_test(lambda u: u.is_staff)
def activate_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_active:
        messages.info(request, "User is already active.")
    else:
        user.is_active = True
        user.save()
        messages.success(request, f"User '{user.username}' has been activated.")
    return redirect('custom_admin:manage_users')


@never_cache
@login_required
@user_passes_test(lambda u: u.is_staff)
def deactivate_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Check for superuser first
    if user.is_superuser:
        messages.error(request, "Cannot deactivate a superuser.")
        return redirect('custom_admin:manage_users')
    
    # Then check if already inactive
    if not user.is_active:
        messages.info(request, "User is already inactive.")
        return redirect('custom_admin:manage_users')
    
    # Finally, deactivate if all checks pass
    user.is_active = False
    user.save()
    messages.success(request, f"User '{user.username}' has been deactivated.")
    return redirect('custom_admin:manage_users')



@login_required
@user_passes_test(lambda u: u.is_staff)
def manage_products_view(request):
    query = request.GET.get('q')
    if query:
        try:
            # Try to convert the query to an integer for ID search
            query_as_int = int(query)
            products = Product.objects.filter(
                Q(product_name__icontains=query) | Q(id=query_as_int)
            )
        except ValueError:
            # If the query is not a valid integer, search only by product name
            products = Product.objects.filter(product_name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, 'custom_admin/manage_products.html', {'products': products})

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('custom_admin:manage_products')  # Redirect to dashboard or product list
    else:
        form = ProductForm(instance=product)
    return render(request, 'custom_admin/edit_product.html', {'form': form, 'product': product})



def delete_product(request, pk):
    try:
        product = get_object_or_404(Product, pk=pk)
    except Product.DoesNotExist:
        return HttpResponseNotFound('<h1>Product not found</h1>')

    if request.method == 'POST':  # Confirm delete
        product.delete()
        return redirect('custom_admin:custom_admin_dashboard')  # Redirect to dashboard or product list
    return render(request, 'custom_admin/delete_product.html', {'product': product})


def add_product(request):
    if request.method == "POST":
        # Retrieve form data
        product_name = request.POST.get('product_name')
        category_id = request.POST.get('category')  # Get the category ID from the form
        subcategory = request.POST.get('subcategory')
        price = request.POST.get('price')
        desc = request.POST.get('desc')
        image = request.FILES.get('image')

        # Fetch the Category instance based on the category_id
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.error(request, "Invalid category selected.")
            return redirect('custom_admin:add_product')

        # Create the product
        Product.objects.create(
            product_name=product_name,
            category=category,  # Use the Category instance
            subcategory=subcategory,
            price=price,
            desc=desc,
            image=image
        )
        messages.success(request, "Product added successfully!")
        return redirect('custom_admin:manage_products')

    # Fetch all categories from the Category model
    categories = Category.objects.all()

    # Pass categories to the template
    context = {
        'categories': categories,
    }
    return render(request, 'custom_admin/add_product.html', context)


from ecommerceapp.models import Slider
from ecommerceapp.forms import SliderForm


@staff_member_required
def slider_dashboard(request):
    sliders = Slider.objects.all()
    return render(request, 'custom_admin/slider_dashboard.html', {'sliders': sliders})

def add_slider(request):
    if request.method == 'POST':
        form = SliderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('custom_admin:slider_dashboard')

    else:
        form = SliderForm()
    return render(request, 'custom_admin/add_slider.html', {'form': form})

def edit_slider(request, pk):
    slider = get_object_or_404(Slider, pk=pk)
    if request.method == 'POST':
        form = SliderForm(request.POST, request.FILES, instance=slider)
        if form.is_valid():
            form.save()
            return redirect('custom_admin:slider_dashboard')
    else:
        form = SliderForm(instance=slider)
    return render(request, 'custom_admin/edit_slider.html', {'form': form, 'slider': slider})

def delete_slider(request, pk):
    slider = get_object_or_404(Slider, pk=pk)
    if request.method == 'POST':
        slider.delete()
        return redirect('custom_admin:slider_dashboard')

    return render(request, 'custom_admin/delete_slider.html', {'slider': slider})





def manage_categories(request):
    categories = Category.objects.all()  # Fetch all categories from the database
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('custom_admin:manage_categories')  # Redirect to the same page after saving
    else:
        form = CategoryForm()
    
    return render(request, 'custom_admin/manage_categories.html', {'form': form, 'categories': categories})

def edit_category(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('custom_admin:manage_categories')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'custom_admin/edit_category.html', context)

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    # Delete the category and its associated products
    category.delete()
    messages.success(request, "Category deleted successfully!")
    
    return redirect('custom_admin:manage_categories')