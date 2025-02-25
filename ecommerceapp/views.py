import stripe
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from ecommerceapp.models import Contact,Product,OrderUpdate,Orders, Slider, Cart, Wishlist, Category
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
from django.db.models import Q
from accounts.models import UserProfile


# @login_required
from math import ceil

def index(request):
   

    # Prepare both product data and slider data for the template
    params = {
       
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
        products = Product.objects.filter(category__slug=val)
        
        # Fetch all categories for the sidebar
        categories = Category.objects.all()
        
        # Context to pass data to the template
        context = {
            'products': products,  # Pass the filtered products
            'slug_value': val,     # Category slug to display in the heading
            'categories': categories,  # Pass all categories for the sidebar
        }
        print("Slug Value:", val)
        print("Products:", products)
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

    # Add a success message
    messages.success(request, f"{product.product_name} has been added to your cart.")

    # Redirect to the "next" URL if provided, otherwise redirect to the product list
    next_url = request.POST.get('next', 'product_list')
    return redirect(next_url)



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
        'total_price': total_price,
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


def search_products(request):
    query = request.GET.get('q')  # Get the search query from the URL parameter
    if query:
        # Use Q objects to search in multiple fields (e.g., product_name and desc)
        products = Product.objects.filter(
            Q(product_name__icontains=query)
        ).distinct()  # Use distinct() to avoid duplicate results
    else:
        products = Product.objects.none()  # Return an empty queryset if no query is provided

    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'products/search_results.html', context)

@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()

    if wishlist_item:
        # If the item is already in the wishlist, remove it
        wishlist_item.delete()
    else:
        # If the item is not in the wishlist, add it
        Wishlist.objects.create(user=request.user, product=product)

    # Redirect to the previous page
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    # Redirect to the previous page
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))

@login_required
def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'products/wishlist.html', context)



stripe.api_key = settings.STRIPE_SECRET_KEY
def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/accounts/login')

    cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
        # Check if the cart is empty
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty. Add items to proceed.")
        return redirect('/list') 

    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        payment_method = request.POST.get('payment_method', 'COD')

        if payment_method == "Stripe":
            try:
                # Create a Stripe Checkout Session
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {'name': 'Cart Items'},
                            'unit_amount': int(total_amount * 100),  # Convert to cents
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri('/checkout/success/') + '?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=request.build_absolute_uri('/checkout/cancel/'),
                )

                return redirect(session.url)

            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
                return redirect('checkout')

        # If payment method is COD, process order directly
        order = Orders.objects.create(
            user=request.user, name=name, email=email, amount=total_amount,
            address1=address1, address2=address2, city=city,
            state=state, zip_code=zip_code, phone=phone,
            payment_method=payment_method,
            payment_status="Pending"  # Default status for COD
        )

        OrderUpdate.objects.create(order=order, update_desc="The order has been placed", payment_status="Pending")
        cart_items.delete()

        return render(request, 'users/order_placed.html', { 'order': order})
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    context = {
        'user': user,
        'user_profile': user_profile,
        'cart_items': cart_items,
        'total_amount': total_amount
    }
    return render(request, 'checkout.html', context)

def checkout_success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        messages.error(request, "Invalid session ID")
        return redirect('checkout')

    try:
        # Retrieve the Stripe session
        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status == 'paid':
            cart_items = Cart.objects.filter(user=request.user)
            total_amount = sum(item.product.price * item.quantity for item in cart_items)

            # Create an order record and mark it as Paid
            order = Orders.objects.create(
                user=request.user,
                name=request.user.get_full_name(),
                email=request.user.email,
                amount=total_amount,
                payment_method="Stripe",
                payment_status="Paid"  # ✅ Set payment as Paid
            )

            # Create an order update record
            OrderUpdate.objects.create(
                order=order,
                update_desc="The order has been placed",
                payment_status="Paid"
            )

            # Clear the cart
            cart_items.delete()
            return render(request, 'users/checkout_success.html')
        else:
            messages.error(request, "Payment not successful")
            return redirect('checkout')

    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('checkout')



def order_summary(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    # Get all orders for the logged-in user
    orders = Orders.objects.filter(user=request.user)

    # Fetch payment status for each order
    for order in orders:
        order_update = OrderUpdate.objects.filter(order_id=order.id).first()
        order.payment_status = order_update.payment_status if order_update else "Unknown"

    return render(request, 'users/order_summary.html', {'orders': orders})


def checkout_cancel(request):
    messages.warning(request, "Payment was cancelled!")
    return redirect('checkout')





stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_stripe_session(request):
    if request.method == "POST":
        try:
            import json
            data = json.loads(request.body)
            amount = int(data.get("amount", 0)) * 100  # Convert to cents

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': 'Cart Items'},
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/checkout/success/') + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri('/checkout/cancel/'),
            )

            return JsonResponse({'session_url': session.url})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



