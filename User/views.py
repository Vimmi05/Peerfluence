from django.shortcuts import render

def UserProfile(request):
    return render(request, 'User/userprofile.html')