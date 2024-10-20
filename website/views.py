from django.shortcuts import render, redirect
from website.models import *
# Create your views here.
def Index(request):
    # posts = Post.objects.all().order_by('-created_at')
    # context = {
    #     'user': request.user,
    #     'posts': posts,
    # }
    return render(request, 'website/index.html')
                #   , context)
def Profile(request):
    return render(request, 'website/profile.html')

def Login(request):
    return render(request, 'website/login.html')