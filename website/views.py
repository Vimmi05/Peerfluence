from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import check_password
# Create your views here.
def Index(request):
    return render(request, 'website/index.html')

def Profile(request):
    return render(request, 'website/profile.html')

def SignUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save the form, but don't commit to the database yet
            user_profile = form.save(commit=False)
            user_profile.password = form.cleaned_data['password']  # Hash this if needed
            user_profile.save()  # Save to the database
            return redirect('/')  # Redirect after successful sign-up
    else:
        form = SignUpForm()

    return render(request, 'website/signup.html', {'form': form})


# def LogIn(request):
    # if request.method == 'POST':
    #     form = CustomAuthenticationForm(request, data=request.POST)
    #     if form.is_valid():
    #         username = form.cleaned_data.get('username')
    #         password = form.cleaned_data.get('password')
    #         user = authenticate(request, username=username, password=password)
    #         if user is not None:
    #             login(request, user)
    #             messages.success(request, 'Logged in successfully!')
    #             return redirect('/')
    #         else:
    #             messages.error(request, 'Invalid username or password')
    # else:
    #     form = CustomAuthenticationForm()
        # return render(request, 'website/login.html')

def LogIn(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user_profile = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            user_profile = None

        user = authenticate(request, email=email, password=password)            
        if user_profile and check_password(password, user_profile.password):
            request.session['user_id'] = user_profile.id
            messages.success(request, 'Logged in successfully!')
            return redirect('/')  # Redirect to the homepage or profile page after login
        else:
            messages.error(request, 'Invalid email or password.')
            print(f"Login failed for email: {email}")
        print(email , password)
    return render(request, 'website/login.html')


def LogOut(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return render(request, 'website/login.html')
