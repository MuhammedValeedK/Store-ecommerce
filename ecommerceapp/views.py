from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from ecommerceapp.models import Contact,Product,OrderUpdate,Orders, Slider, Cart
from django.contrib import messages
from math import ceil
# from ecommerceapp import keys
from django.conf import settings
# MERCHANT_KEY=keys.MK
import json
from django.views.decorators.csrf import  csrf_exempt
# from PayTm import Checksum
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from itertools import count




# @login_required
from math import ceil

def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    # Prepare both product data and slider data for the template
    params = {
        'allProds': allProds,
        'sliders': Slider.objects.all()  # Include slider data
    }

    # Pass a single combined dictionary to the render function
    return render(request, "index.html", params)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

class category_view(View):
    def get(self, request, val):
        # Filter products by the given category slug
        products = Product.objects.filter(category=val)
        
        # Context to pass data to the template
        context = {
            'products': products,  # Pass the filtered products
            'slug_value': val,     # Category slug to display in the heading
        }
        return render(request, "products/category.html", context)




def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        desc=request.POST.get("desc")
        pnumber=request.POST.get("pnumber")
        myquery=Contact(name=name,email=email,desc=desc,phonenumber=pnumber)
        myquery.save()
        messages.info(request,"we will get back to you soon..")
        return render(request,"contact.html")


    return render(request,"contact.html")


def about(request):
    return render(request, "about.html")


def get_product(request):
    return render(request,"products/product.html")

def product_list(request):
    # Fetch products (replace this with your actual logic)
    products = Product.objects.all()

    # Calculate the cart count for the current user
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
    else:
        cart_count = 0

    context = {
        'products': products,
        'cart_count': cart_count,  # Pass the cart count to the template
    }
    return render(request, 'products/product_list.html', context)



@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('product_list')



def view_cart(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/accounts/login')

    cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    
    # Calculate the total price for each item and the overall total
    for item in cart_items:
        item.total_price = item.product.price * item.quantity  # Add a total_price attribute to each item

    total_price = sum(item.total_price for item in cart_items)  # Calculate the overall total
    
    # Calculate the cart count
    cart_count = cart_items.count()

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'cart_count': cart_count,  # Pass the cart count to the template
        }
    return render(request, 'products/cart.html', context)



def clear_cart(request):
        # Fetch all cart items for the current user
    cart_items = Cart.objects.filter(user=request.user)
        # Delete all cart items
    cart_items.delete()
        # Add a success message
    messages.success(request, "Your cart has been cleared.")
        # Redirect to the cart page
    return redirect('view_cart')



def remove_from_cart(request, item_id):
    # Fetch the cart item
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
        # Delete the cart item
    cart_item.delete()
        # Add a success message
    messages.success(request, "Item removed from your cart.")
        # Redirect to the cart page
    return redirect('view_cart')


def update_cart(request, item_id):
    if request.method == 'POST':
        # Fetch the cart item
        cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
                # Get the new quantity from the form
        new_quantity = int(request.POST.get('quantity'))
            # Update the quantity
        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, "Cart updated successfully.")
        else:
            cart_item.delete()
            messages.success(request, "Item removed from your cart.")
        # Redirect to the cart page
    return redirect('view_cart')



def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/accounts/login')

    cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        order = Orders(
            items_json=items_json,
            name=name,
            amount=total_amount,
            email=email,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone,
            user=request.user
        )
        order.save()

        update = OrderUpdate(order_id=order.id, update_desc="The order has been placed")
        update.save()

        cart_items.delete()  # Clear the cart
        thank = True
        return render(request, 'checkout.html', {'thank': thank, 'order': order})

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
    }
    return render(request, 'checkout.html', context)



def razorpaycheck(request):
    cart = Product.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price =  total_price + item.product.price * item.quantity
    
    return JsonResponse({
        'total_price': total_price
    })




@csrf_exempt
def proceed_to_pay(request):
    if request.method == 'POST':
        try:
            data = request.POST
            cart = json.loads(data.get('cart', '{}'))
            total_price = data.get('total_price', 0)

            # Process the data (e.g., store it in the database or initiate Razorpay order creation)
            return JsonResponse({'status': 'success', 'message': 'Payment initiated', 'total_price': total_price})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)