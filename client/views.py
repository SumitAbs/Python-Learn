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
import numpy as np
from django.http import JsonResponse
import pandas as pd



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
           
            # messages.success(request, "Login successful!")
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
 
 
def numpy_example(request):
    # 1D NumPy Array
    arr = np.array([1, 2, 3, 4, 5])
    
    # NumPy ka mean calculate karna
    mean_value = np.mean(arr)

    # Random matrix generate karna
    random_matrix = np.random.randint(1, 100, (1, 3)).tolist()

    return JsonResponse({
        'array': arr.tolist(),
        'mean': mean_value,
        'random_matrix': random_matrix
    })
    
def matrix_multiplication(request):
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])

    result = np.dot(A, B)  # ✅ NumPy se matrix multiplication
    return JsonResponse({"result": result.tolist()})

def ArrayCreationFunctions(request):
    arr = np.array([1, 2, 3, 4, 5])  # Basic NumPy array
    zeros_arr = np.zeros((2, 2))  # 2x2 matrix of zeros
    ones_arr = np.ones((2, 2))  # 2x2 matrix of ones
    full_arr = np.full((2, 2), 7)  # 2x2 matrix filled with 7
    range_arr = np.arange(1, 10, 3)  # [1, 3, 5, 7, 9]
    linspace_arr = np.linspace(0, 10, 5)  # [0, 2.5, 5, 7.5, 10]
    identity_matrix = np.eye(3)  # 3x3 identity matrix
    rand_matrix = np.random.rand(2, 2)  # Random float numbers between 0 and 1
    randint_matrix = np.random.randint(1, 100, (3, 3))  # 3x3 random integers
    return JsonResponse({
        'array': arr.tolist(),
        'zeros_arr': zeros_arr.tolist(),
        'ones_arr': ones_arr.tolist(),
        'full_arr_with7': full_arr.tolist(),
        'range_arr': range_arr.tolist(),
        'linspace_arr': linspace_arr.tolist(),
        'identity_matrix': identity_matrix.tolist(),
        'rand_matrix': rand_matrix.tolist(),
        'randint_matrix': randint_matrix.tolist(),
    })
    
def ArrayManipulationFunctions(request):
    arr = np.array([1, 2, 3, 4, 5])  # Basic NumPy array
    range_arr = np.arange(1, 10, 2)  # [1, 3, 5, 7, 9]
    reshaped_arr = np.reshape(arr, (5, 1))  # Convert 1D to 2D
    flattened_arr = np.array([[1, 2], [3, 4]]).flatten()  # Convert 2D to 1D
    concatenated_arr = np.concatenate((arr, range_arr))  # Concatenating arrays
    vstack_arr = np.vstack((arr, arr))  # Vertical stacking
    hstack_arr = np.hstack((arr, arr))  # Horizontal stacking
    split_arr = np.split(arr, 5)  # Split array into 5 parts
    expanded_arr = np.expand_dims(arr, axis=0)  # Add new dimension
    return JsonResponse({
        'reshaped_arr': reshaped_arr.tolist(),
        'flattened_arr': flattened_arr.tolist(),
        'concatenated_arr': concatenated_arr.tolist(),
        'vstack_arr': vstack_arr.tolist(),
        'hstack_arr': hstack_arr.tolist(),
        'split_arr': [s.tolist() for s in split_arr],
        'expanded_arr': expanded_arr.tolist(),
    })
    
def MathematicalFunctions(request):
    arr = np.array([1, 2, 3, 4, 5])  # Basic NumPy array
    added_arr = np.add(arr, 10)  # Add 10 to each element
    subtracted_arr = np.subtract(arr, 2)  # Subtract 2 from each element
    multiplied_arr = np.multiply(arr, 2)  # Multiply each element by 2
    divided_arr = np.divide(arr, 2)  # Divide each element by 2
    power_arr = np.power(arr, 2)  # Square each element
    mod_arr = np.mod(arr, 3)  # Remainder when divided by 3
    exp_arr = np.exp(arr)  # Exponential of each element
    sqrt_arr = np.sqrt(arr)  # Square root of each element
    return JsonResponse({
        'added_arr': added_arr.tolist(),
        'subtracted_arr': subtracted_arr.tolist(),
        'multiplied_arr': multiplied_arr.tolist(),
        'divided_arr': divided_arr.tolist(),
        'power_arr': power_arr.tolist(),
        'mod_arr': mod_arr.tolist(),
        'exp_arr': exp_arr.tolist(),
        'sqrt_arr': sqrt_arr.tolist(),
    })
     
def StatisticalFunctions(request):
    arr = np.array([1, 2, 3, 4, 5])  # Basic NumPy array

    # Convert NumPy types to Python native types
    mean_value = float(np.mean(arr))  # Convert to float
    median_value = float(np.median(arr))  # Convert to float
    std_dev = float(np.std(arr))  # Convert to float
    variance = float(np.var(arr))  # Convert to float
    min_value = int(np.min(arr))  # Convert to int
    max_value = int(np.max(arr))  # Convert to int
    sum_value = int(np.sum(arr))  # Convert to int
    cumulative_sum = np.cumsum(arr)  # Convert to a Python list
    return JsonResponse({
        'mean_value': mean_value,
        'median_value': median_value,
        'std_dev': std_dev,
        'variance': variance,
        'min_value': min_value,
        'max_value': max_value,
        'sum_value': sum_value,
        'cumulative_sum': cumulative_sum.tolist(),
    })

def RandomNumberGeneration(request):
    arr = np.array([1, 2, 3, 4, 5])  # Basic NumPy array
    uniform_random = np.random.rand(3)  # 3 random numbers between 0-1
    normal_random = np.random.randn(3)  # 3 numbers from normal distribution
    randint_random = np.random.randint(1, 10, (2, 2))  # 2x2 matrix of random integers
    choice_random = np.random.choice(arr)  # Random element from array
    shuffled_arr = np.random.permutation(arr)  # Shuffle array
    return JsonResponse({
        'uniform_random': uniform_random.tolist(),
        'normal_random': normal_random.tolist(),
        'randint_random': randint_random.tolist(),
        'choice_random': choice_random.tolist(),
        'shuffled_arr': shuffled_arr.tolist(),
    })

def SortingSearching(request):
    arr = np.array([1, 2, 3, 4, 5])  # Basic NumPy array
    sorted_arr = np.sort(arr)  # Sort array
    argsorted_indices = np.argsort(arr)  # Indices of sorted elements
    max_index = np.argmax(arr)  # Index of max value
    min_index = np.argmin(arr)  # Index of min value
    unique_elements = np.unique([1, 2, 2, 3, 3, 3, 4])  # Find unique values
    return JsonResponse({
        'sorted_arr': sorted_arr.tolist(),
        'argsorted_indices': argsorted_indices.tolist(),
        'max_index': max_index,
        'min_index': min_index,
        'unique_elements': unique_elements.tolist(),
    })
    
def BooleanLogicalOperations(request):
    arr = np.array([1, 2, 3, 4, 5])  # Basic NumPy array
    all_positive = np.all(arr > 0)  # Check if all elements are positive
    any_negative = np.any(arr < 0)  # Check if any element is negative
    logical_and_result = np.logical_and(arr > 2, arr < 5)  # Logical AND operation
    logical_or_result = np.logical_or(arr < 2, arr > 4)  # Logical OR operation
    logical_not_result = np.logical_not(arr > 3)  # Logical NOT operation

    return JsonResponse({
        'all_positive': all_positive,
        'any_negative': any_negative,
        'logical_and_result': logical_and_result.tolist(),
        'logical_or_result': logical_or_result.tolist(),
        'logical_not_result': logical_not_result.tolist(),
    })
    
def PandasExamples(request):
    # Creating a Series (1D Data)
    series = pd.Series([10, 20, 30, 40, 50])
    
    # Creating a DataFrame (2D Table)
    data = {
        'Name': ['Ali', 'Sara', 'Ahmed', 'Zoya'],
        'Age': [23, 25, 22, 24],
        'City': ['Lahore', 'Karachi', 'Islamabad', 'Faisalabad']
    }
    df = pd.DataFrame(data)

    # Basic Statistics
    mean_age = int(df['Age'].mean())  # Convert to int
    median_age = int(df['Age'].median())  # Convert to int
    std_dev_age =  (df['Age'].std())  # Convert to float (can be decimal)
    min_age = int(df['Age'].min())  # Convert to int
    max_age = int(df['Age'].max())  # Convert to int
    
    # Filtering Data (Age > 23)
    adults = df[df['Age'] > 23].to_dict(orient='records')
    
    # Sorting Data (Descending Order by Age)
    sorted_df = df.sort_values(by='Name', ascending=False).to_dict(orient='records')
    
    # Adding a New Column
    df['Salary'] = [50000, 60000, 55000, 58000]
    df_with_salary = df.to_dict(orient='records')
    
    # Convert numeric values to Python int for JSON serialization
    grouped = df.groupby('Name')[['Age', 'Salary']].mean().applymap(lambda x: int(x)).to_dict()
    
    # Dropping a Column
    df_dropped = df.drop(columns=['Salary']).to_dict(orient='records')
    
    # Converting DataFrame to Dictionary
    df_dict = df.to_dict()
    
    return JsonResponse({
        'series': series.tolist(),
        'dataframe': df.to_dict(orient='records'),
        'mean_age': mean_age,
        'median_age': median_age,
        'std_dev_age': std_dev_age,
        'min_age': min_age,
        'max_age': max_age,
        'filtered_adults': adults,
        'sorted_by_age': sorted_df,
        'dataframe_with_salary': df_with_salary,
        'grouped_by_city': grouped,
        'dataframe_without_salary': df_dropped,
        'dataframe_dict': df_dict
    })