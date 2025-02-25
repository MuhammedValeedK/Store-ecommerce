from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from .models import UserProfile
from ecommerceapp.models import Orders, OrderUpdate, Wishlist
import json
# Create your views here.




def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()  # Collect username
        email = request.POST.get('email', '').strip()
        password = request.POST.get('pass1', '')
        confirm_password = request.POST.get('pass2', '')

        # Basic validation
        if not username or not email or not password or not confirm_password:
            messages.warning(request, "Please fill all the required fields.")
            return render(request, 'accounts/signup.html')

        if password != confirm_password:
            messages.warning(request, "Passwords don't match.")
            return render(request, 'accounts/signup.html')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username is already taken.")
            return render(request, 'accounts/signup.html')

        if User.objects.filter(email=email).exists():
            messages.warning(request, "An account with this email already exists.")
            return render(request, 'accounts/signup.html')

        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.is_active = False
            user.save()

            # Generate activation email
            current_site = get_current_site(request)
            email_subject = "Activate Your Account"
            message = render_to_string('accounts/activate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })

            # Send activation email
            try:
                email_message = EmailMessage(
                    email_subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email]
                )
                email_message.send()
                messages.success(request, "Please check your email to activate your account.")
            except Exception as e:
                user.delete()  # Delete user if email sending fails
                messages.error(request, "Failed to send activation email. Please try again.")
                return render(request, 'accounts/signup.html')

            return redirect('login')  # Assuming 'login' is your URL name

        except Exception as e:
            messages.error(request, "An error occurred during registration. Please try again.")
            return render(request, 'accounts/signup.html')

    return render(request, 'accounts/signup.html')

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been activated successfully!")
            return redirect('login')
        else:
            messages.error(request, "Activation link is invalid or has expired!")
            return redirect('signup') 



def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get('email', '').strip()  # Accepts username or email
        userpassword = request.POST.get('pass1', '').strip()

        # Check if the identifier is an email or username
        try:
            if '@' in identifier:
                user = User.objects.get(email=identifier)
                username = user.username
            else:
                username = identifier
        except User.DoesNotExist:
            messages.error(request, "Invalid credentials. User not found.")
            return redirect('/accounts/login')

        # Authenticate the user
        myuser = authenticate(username=username, password=userpassword)

        if myuser is not None:
            UserProfile.objects.get_or_create(user=myuser)
            login(request, myuser)
            messages.success(request, "Login Successful")

            # Redirect superuser to custom admin page
            if myuser.is_superuser:
                return redirect('/custom_admin/')  # Adjust the URL as needed

            # Redirect regular users to homepage
            return redirect('/')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('/accounts/login')

    return render(request, 'accounts/login.html')




def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out")
    return redirect('/accounts/login')


from .forms import UserUpdateForm, ProfileUpdateForm

@login_required
def profile(request):
    # Ensure the user has a UserProfile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            if user_form.has_changed() or profile_form.has_changed():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile has been updated successfully!')
                return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
      # Fetch user orders and wishlist
    orders = Orders.objects.filter(user=request.user).order_by('-id')
    wishlist_items = Wishlist.objects.filter(user=request.user)
    for order in orders:
        try:
            order.items = json.loads(order.items_json)  # ✅ Parse JSON safely
        except json.JSONDecodeError:
            order.items = []  # If JSON is invalid, assign an empty list
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_profile': user_profile,
        'orders': orders,
        'wishlist_items': wishlist_items
    }
    return render(request, 'users/profile.html', context)