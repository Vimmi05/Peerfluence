from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Skill, UserInformation
from .forms import SkillForm, UserInformationForm, forms
from django.contrib import messages


def UserProfile(request):
    if request.method == 'POST':
        form = UserInformationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()  
            return redirect('profile') 
    else:
        form = UserInformationForm()  

    return render(request, 'User/userprofile.html', {'form': form})

def UpdateUserProfile(request, id):
    # Use get_object_or_404 to handle cases where the UserInformation does not exist
    data = get_object_or_404(UserInformation, id=id)
    print(f"User ID: {data.id}")

    form = UserInformationForm(instance=data)  # Create a form instance with existing data

    if request.method == "POST":
        form = UserInformationForm(request.POST,request.FILES, instance=data)  # Bind form with POST data
        if form.is_valid():
            form.save()  # Save changes to the database
            messages.success(request, "Data successfully updated!")
            return redirect('profile')  # Redirect to the profile view or another relevant page
        else:
            messages.error(request, "Please correct the errors below.")  # Notify about form errors


    context = {'form': form, 'data': data}  # Prepare context for rendering the template
    print(context)

    return render(request, 'User/update_profile.html', context)  # Render the update profile template

def manage_skills(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new skill
            return redirect('profile')  # Redirect to a success URL
    else:
        form = SkillForm()  # Initialize an empty form

    return render(request, 'User/manage_skills.html', {'form': form})