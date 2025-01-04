from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from User.models import *
from Article.models import *
from Article.forms import *
import random

# Create your views here.
def Index(request):
    username = None
    status = None
    college = None
    # Check if the user ID is in the session

    # notification_messages = [
    #     "username1 has sent you a follow request",
    #     "username2 has sent you a follow request",
    #     "Welcome to Peerfluence, begin your journey!",
    #     "You have a new message",
    #     "Your post has been liked",
    #     "A new event is coming up",
    # ]
    # random_count = random.randint(1, len(notification_messages))
    # notifications = random.sample(notification_messages, random_count)
    random_posts = UserPostModel.objects.order_by('?')

    user_info = UserInformation.objects.order_by('-created_at').first()
    state = user_info.state
    img = user_info.img


    user_all = UserProfile.objects.order_by('?')[:3]

    if 'user_id' in request.session:
        try:
            user_profile = UserProfile.objects.get(id=request.session['user_id'])
            username = f"{user_profile.first_name} {user_profile.last_name}"
            college = user_profile.college
            status = user_profile.current_status

            random_user = UserProfile.objects.order_by('?').first()
            random_username = f"{random_user.first_name} {random_user.last_name}" if random_user else "Someone"
            notification_messages = [
                f"{random_username} has sent you a follow request",
                "Welcome to Peerfluence, begin your journey!",
                "You have a new message",
                "Your post has been liked",
                "A new event is coming up",
            ]

            # Get the first name from UserProfile
        except UserProfile.DoesNotExist:
            # Handle case where the UserProfile does not exist
            messages.error(request, 'User profile not found.')
            del request.session['user_id']  # Clear session if user profile not found
    else:
        messages.info(request, 'You are not logged in.')

    random_count = random.randint(1, len(notification_messages))
    notifications = random.sample(notification_messages, random_count)
    data = ArticleModels.objects.all()

    context = {
        'username': username,
        'status': status,
        'college': college,
        'data':data,
        'random_posts':random_posts,
        'state':state,
        'user_all':user_all,
        'img':img,
        'random_count':random_count,
        'notifications': notifications,        
    }
    return render(request, 'website/index.html', context)

def Profile(request):
    username = None
    student_id = None
    status = None
    college = None
    passout_year = None
    employee_id = None
    email = None
    phone = None
    gender = None

    # Initialize notifications and random_count
    notification_messages = []
    random_count = 0

    if 'user_id' in request.session:
        try:
            user_profile = UserProfile.objects.get(id=request.session['user_id'])

            posts = UserPostModel.objects.filter(user_profile=user_profile)
            post_count = posts.count()
            image_count = sum(1 for post in posts if post.img)

            username = f"{user_profile.first_name} {user_profile.last_name}"
            college = user_profile.college
            status = user_profile.current_status
            student_id = user_profile.student_id
            passout_year = user_profile.passout_year
            employee_id = user_profile.employee_id
            email = user_profile.email
            phone = user_profile.phone
            gender = user_profile.gender

            # NOTIFICATIONS
            random_user = UserProfile.objects.order_by('?').first()
            random_username = f"{random_user.first_name} {random_user.last_name}" if random_user else "Someone"

            notification_messages = [
                f"{random_username} has sent you a follow request",
                "Welcome to Peerfluence, begin your journey!",
                "You have a new message",
                "Your post has been liked",
                "A new event is coming up",
            ]

            # Randomly select notifications
            random_count = random.randint(1, len(notification_messages))
            notifications = random.sample(notification_messages, random_count)

        except UserProfile.DoesNotExist:
            messages.error(request, 'User profile not found.')
            del request.session['user_id']
    else:
        messages.info(request, 'You are not logged in.')

    # PROFILE INFO
    user_info = UserInformation.objects.order_by('-created_at').first()
    img = user_info.img
    profession = user_info.profession
    birthday = user_info.birthday
    country = user_info.country
    state = user_info.state
    city = user_info.city
    languages = user_info.languages
    interests_music = user_info.interests_music
    interests_movies = user_info.interests_movies
    description = user_info.description

    # FOLLOW
    followers = random.randint(0, 10)
    following = random.randint(0, 10)

    user_all = UserProfile.objects.exclude(id=user_profile.id).order_by('?')[:followers]

    # SKILLS
    skills = Skill.objects.order_by('?')[:4]

    # CONTEXT
    context = {
        'username': username,
        'status': status,
        'college': college,
        'student_id': student_id,
        'passout_year': passout_year,
        'employee_id': employee_id,
        'email': email,
        'phone': phone,
        'img': img,
        'profession': profession,
        'birthday': birthday,
        'country': country,
        'state': state,
        'city': city,
        'languages': languages,
        'interests_music': interests_music,
        'interests_movies': interests_movies,
        'description': description,
        'followers': followers,
        'following': following,
        'data': user_info,
        'user': f"{user_profile.first_name} {user_profile.last_name}",
        'posts': posts,
        'post_count': post_count,
        'image_count': image_count,
        'user_all': user_all,
        'gender': gender,
        'skills': skills,
        'notifications': notifications,  # Pass notifications to the template
        'random_count': random_count,  # Pass random_count to the template
    }

    return render(request, 'website/profile.html', context)


def SignUp(request):
    if request.method == 'POST':
        print(request.POST) 
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save the form, but don't commit to the database yet
            user_profile = form.save(commit=False)
            user_profile.password = form.cleaned_data['password']  # Hash this if needed
            user_profile.save()  # Save to the database
            return redirect('login')  # Redirect after successful sign-up
        else:
            print(form.errors)
    else:
        form = SignUpForm()

    return render(request, 'website/signup.html', {'form': form})

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

def create_post(request):
    username = None

    if request.method == 'POST':
        user_profile = UserProfile.objects.get(id=request.session['user_id'])
        form = UserPostForm(request.POST, request.FILES, user_profile=user_profile)

        if form.is_valid():
            post = form.save(commit=False)
            post.user_profile = user_profile
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('/')
    else:
        user_profile = UserProfile.objects.get(id=request.session['user_id'])
        form = UserPostForm(user_profile=user_profile)
        username = f"{user_profile.first_name} {user_profile.last_name}"

    context = {
        'form': form,
        'username': username,
    }

    return render(request, 'website/user_post.html', context)

# def user_posts(request):
#     user_profile = UserProfile.objects.get(id=request.session['user_id'])
#     posts = UserPostModel.objects.filter(user_profile=user_profile)
#     print(f"User: {user_profile}, Posts: {posts.count()}")
#     context = {
#         'username': f"{user_profile.first_name} {user_profile.last_name}",
#         'posts': posts,
#     }

#     return render(request, 'website/profile.html', context)

# def manage_skills(request):
#     # Your logic to get the skills and render the manage skills page
#     return render(request, 'User/manage_skills.html')