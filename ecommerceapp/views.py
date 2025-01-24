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
        context = {'slug_value': val,}  # Example context to pass to the template
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


import json

@login_required
def sync_cart(request):
    if request.method == 'POST':
        cart_data = json.loads(request.POST.get('cart_data'))
        
        # Clear existing cart items for this user
        Cart.objects.filter(user=request.user).delete()
        
        # Add items from localStorage to database
        for product_id, item_data in cart_data.items():
            try:
                product = Product.objects.get(id=product_id)
                Cart.objects.create(
                    user=request.user,
                    product=product,
                    quantity=item_data['qty']
                )
            except Product.DoesNotExist:
                continue
                
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.get_total() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'cart.html', context)





def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/accounts/login')

    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        Order = Orders(items_json=items_json,name=name,amount=amount, email=email, address1=address1,address2=address2,city=city,state=state,zip_code=zip_code,phone=phone)
        print(amount)
        Order.save()
        update = OrderUpdate(order_id=Order.order_id,update_desc="the order has been placed")
        update.save()
        thank = True


    return render(request, 'checkout.html')

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