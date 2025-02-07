from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout as auth_logout
from client.models import User
from django.core.mail import send_mail
from django.urls import reverse

from django.core.signing import TimestampSigner
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model



# Create your views here.
def index(request):
    return render(request, 'client/index.html')  # This is the root path

def about(request):
    return render(request, 'client/about.html') # This is the about path

def contact(request):
    return render(request, 'client/contact.html') # This is the contact path


# def signup(request):
#     return render(request, 'client/auth/signup.html') # This is the signup path 

# Signup view function
def signup(request):
    if request.method == 'POST':
        # Get data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')
        
         # Ensure the username/email does not already exist
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return redirect('signup')

        # Create the user object
        user = User.objects.create(
            first_name=first_name, last_name=last_name, email=email,
            username=username, phone=phone, address=address
        )
        # Encrypt the password
        user.set_password(password)
        user.save()
        messages.success(request, "Account created successfully!")
        return redirect('login')  # Redirect to login or another page after successful signup

    return render(request, 'client/auth/signup.html')  # Return the form if the request method is GET


# def login(request):
#     return render(request, 'client/auth/login.html') # This is the login path
def set_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, email=email, password=password)
        
        # if check_password(password, user.password):
        if user is not None:
            login(request, user)
            # Successful login, set user as authenticated
           
            messages.success(request, "Login successful!")
            return redirect('cdashboard')  
        else:
            # Invalid credentials
            messages.error(request, "Invalid email or password...")

    return render(request, 'client/auth/login.html')  # Render the login form if it's a GET request

def cdashboard(request):
    if not request.user.is_authenticated:
        return redirect('set_login')
    username = request.user.username
    return render(request, 'client/dashboard.html', {'username': username})  # Render the dashboard with username

    # if request.session.exists(request.session.session_key):
        # session_data = request.session.items()
        # session_values = {key: value for key, value in session_data}
        # return HttpResponse(f"Welcome to the home page. Session data: {session_values}")
    # else:
    #     return redirect('set_login')

def logout(request):
    auth_logout(request)  # This will end the user's session
    return redirect('set_login')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('set_login')
    
    if request.method == 'POST':
        first_name  =   request.POST.get('first_name')
        last_name   =   request.POST.get('last_name')
        email       =   request.POST.get('email')
        password    =   request.POST.get('password')
        confirm_password    =   request.POST.get('confirm_password')
        phone       =   request.POST.get('phone')
        address     =   request.POST.get('address')
        
        # Check if the password and confirm password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match...")
            return redirect('profile')
        
        # Update the user's profile
        user            =   request.user
        user.first_name =   first_name
        user.last_name  =   last_name
        user.email      =   email
        user.phone      =   phone
        user.address    =   address
        # Encrypt the password
        user.set_password(password)
        user.save()
        messages.success(request, "Profile updated successfully!")

    return render(request, 'client/auth/profile.html')  # This is the profile path

def delete_profile(request):
    user = request.user
    user.delete()
    messages.success(request, "Profile deleted successfully!")
    return redirect('login') # This is the delete_profile path

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Check if the email exists in the database
        User = get_user_model()
        user = User.objects.get(email=email)
        if user:
            uidb64, token = generate_password_reset_token(user)
            reset_link = request.build_absolute_uri(
                reverse('reset-password', kwargs={'uidb64': uidb64, 'token': token})
            )
            message = f"Hello {user.username},\n\nClick the link below to reset your password:\n{reset_link}\n\nIf you didn't request this, ignore this email."
            
            # Send a password reset email to the user
            subject = 'Test Email'
            recipient_list = [email]
            
            send_mail(subject, message, None, recipient_list)
            
            messages.success(request, "Change password link sent to your email...")
            return redirect('set_login')
        else:
            messages.error(request, "Email does not exist...")
    return render(request, 'client/auth/forgotPassword.html') # This is the forgot_password path

def generate_password_reset_token(user):
    signer = TimestampSigner()
    token = signer.sign(user.email)  # Signing user email for security
    return urlsafe_base64_encode(force_bytes(user.email)), token

def reset_password(request,uidb64, token):
    signer = TimestampSigner()
    uid = urlsafe_base64_decode(uidb64).decode()
    user = get_user_model().objects.get(email=uid)

    # Verify the token
    original_token = signer.unsign(token, max_age=3600)  # 1-hour expiration
    # return HttpResponse(f"Welcome to the home page. Session data: {original_token}")
    
    if str(user.email) == original_token:
        if request.method == "POST":
            password = request.POST["password"]
            confirm_password = request.POST["confirm_password"]
                # Check if the password and confirm password match
            if password != confirm_password:
                messages.error(request, "Passwords do not match...")
                return render(request, "client/auth/changePassword.html")
            
            user.set_password(password)
            user.save()
            messages.success(request, "Passwords Updated Successfully...")
            return redirect("set_login")  # Redirect after successful password reset
    return render(request, "client/auth/changePassword.html")
    # except Exception:
    #     return HttpResponse(f"Welcome to the home page. no Session data:")
    #     return render(request, "client/auth/changePassword.html")
 