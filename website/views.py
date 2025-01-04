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

    # Initialize notification_messages with a default value
    notification_messages = [
        "Welcome to Peerfluence, begin your journey!",
        "You have a new message",
        "Your post has been liked",
        "A new event is coming up",
    ]

    # Fetch random posts
    random_posts = UserPostModel.objects.order_by('?')

    # Fetch user information
    user_info = UserInformation.objects.order_by('-created_at').first()
    state = user_info.state if user_info else None
    img = user_info.img if user_info else None

    # Fetch 3 random users for "Suggestions for You"
    random_users = UserProfile.objects.order_by('?')[:3]

    # Handle search query
    search_query = request.GET.get('q')
    if search_query:
        # Filter users based on search query
        user_all = UserProfile.objects.filter(
            first_name__icontains=search_query
        ) | UserProfile.objects.filter(
            last_name__icontains=search_query
        )
    else:
        # If no search query, use the random users for search results (optional)
        user_all = UserProfile.objects.none()  # Empty queryset by default

    if 'user_id' in request.session:
        try:
            user_profile = UserProfile.objects.get(id=request.session['user_id'])
            username = f"{user_profile.first_name} {user_profile.last_name}"
            college = user_profile.college
            status = user_profile.current_status

            random_user = UserProfile.objects.order_by('?').first()
            random_username = f"{random_user.first_name} {random_user.last_name}" if random_user else "Someone"

            # Update notification_messages if the user is logged in
            notification_messages = [
                f"{random_username} has sent you a follow request",
                "Welcome to Peerfluence, begin your journey!",
                "You have a new message",
                "Your post has been liked",
                "A new event is coming up",
            ]

        except UserProfile.DoesNotExist:
            # Handle case where the UserProfile does not exist
            messages.error(request, 'User profile not found.')
            del request.session['user_id']
    else:
        messages.info(request, 'You are not logged in.')

    # Calculate random_count and notifications only if notification_messages is not empty
    if notification_messages:
        random_count = random.randint(1, len(notification_messages))
        notifications = random.sample(notification_messages, random_count)
    else:
        random_count = 0
        notifications = []

    # Fetch articles
    data = ArticleModels.objects.all()

    context = {
        'username': username,
        'status': status,
        'college': college,
        'data': data,
        'random_posts': random_posts,
        'state': state,
        'user_all': user_all,  # Users matching the search query
        'random_users': random_users,  # Random users for "Suggestions for You"
        'img': img,
        'random_count': random_count,
        'notifications': notifications,
        'search_query': search_query,
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

            # Generate random followers count
            followers_count = random.randint(0, 10)
            request.session['followers_count'] = followers_count  # Store in session

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
    followers = request.session.get('followers_count', 0)  # Retrieve from session
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
        'notifications': notifications,
        'random_count': random_count,
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

def Followers(request):
    context = {}

    if 'user_id' in request.session:
        try:
            user_profile = UserProfile.objects.get(id=request.session['user_id'])
            
            # Retrieve the followers count from the session
            followers_count = request.session.get('followers_count', 0)
            
            # Fetch a random set of followers matching the count
            followers = UserProfile.objects.exclude(id=user_profile.id).order_by('?')[:followers_count]
            
            # Add followers to the context
            context['followers'] = followers
            context['followers_count'] = followers_count

        except UserProfile.DoesNotExist:
            messages.error(request, 'User profile not found.')
            del request.session['user_id']
    else:
        messages.info(request, 'You are not logged in.')

    return render(request, 'website/followers.html', context)