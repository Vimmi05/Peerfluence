from django.shortcuts import render, redirect

# Create your views here.
def Index(request):
    return render(request, 'website/index.html')
