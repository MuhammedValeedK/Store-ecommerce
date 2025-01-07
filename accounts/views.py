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
# Create your views here.



# def signup_view(request):
#     if request.method == "POST":
#         email = request.POST['email']
#         password = request.POST['pass1']
#         confirm_password = request.POST['pass2']

#         if password != confirm_password:
#             messages.warning(request, "Password doesn’t match.")
#             return render(request, 'accounts/signup.html')

#         try:
#             if User.objects.get(username=email):
#                 messages.info(request, "Email exists already")
#                 return render(request, 'accounts/signup.html')
#         except User.DoesNotExist:
#             pass  # User with this email doesn't exist, proceed with creating a new user

#         user = User.objects.create_user(email, email, password)
#         user.is_active = False 
        
#         user.save()

#         email_subject = "Activate Your Account"
#         message = render_to_string('accounts/activate.html', {
#             'user': user,
#             'domain': '127.0.0.1:8000', 
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             'token': generate_token.make_token(user)
#         })

#         # Uncomment and configure email sending logic when ready
#         email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
#         email_message.send()

#         messages.success(request, f"Activate Your Account by clicking the link in your gmail")
#         return redirect('/accounts/login/')

#     return render(request, "accounts/signup.html")

# # class ActivateAccountView(View):
#     def get(self,request,uidb64,token):
#         try:
#             uid=force_str(urlsafe_base64_decode(uidb64))
#             user=User.objects.get(pk=uid)
#         except Exception as identifier:
#             user=None
#         if user is not None and generate_token.check_token(user,token):
#             user.is_active=True
#             user.save()
#             messages.info(request,"Account Activated Successfully")
#             return redirect('/accounts/login')
#         return render(request,'/accounts/activatefail.html')


from django.contrib.sites.shortcuts import get_current_site
def signup_view(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        password = request.POST.get('pass1', '')
        confirm_password = request.POST.get('pass2', '')

        # Basic validation
        if not email or not password or not confirm_password:
            messages.warning(request, "Please fill all the required fields.")
            return render(request, 'accounts/signup.html')

        if password != confirm_password:
            messages.warning(request, "Passwords don't match.")
            return render(request, 'accounts/signup.html')

        # Check if user exists
        if User.objects.filter(email=email).exists():
            messages.warning(request, "An account with this email already exists.")
            return render(request, 'accounts/signup.html')

        try:
            # Create user
            user = User.objects.create_user(
                username=email,
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
            return redirect('signup')  # Assuming 'signup' is your URL name




def login_view(request):
    if request.method=="POST":

        username=request.POST['email']
        userpassword=request.POST['pass1']
        myuser=authenticate(username=username,password=userpassword)

        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Success")
            return redirect('/')

        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/accounts/login')

    return render(request,'accounts/login.html')  




def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out")
    return redirect('/accounts/login')

