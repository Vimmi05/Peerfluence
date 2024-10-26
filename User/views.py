from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserInformation
from .forms import UserInformationForm

def UserProfile(request):
    if request.method == 'POST':
        form = UserInformationForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('profile') 
    else:
        form = UserInformationForm()  

    return render(request, 'User/userprofile.html', {'form': form})
