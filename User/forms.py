from django import forms
from .models import UserInformation
from django.forms import modelformset_factory
from .models import Skill

class UserInformationForm(forms.ModelForm):
    class Meta:
        model = UserInformation
        # fields = [ 'passout_year', 'profession', 'college', 
                #   'birthday', 'country', 'state', 'city', 'languages', 
                #   'email', 'phone', 'interests_music', 'interests_movies']
        
        fields = [ 'profession', 'img',
                  'birthday', 'country', 'state', 'city', 'languages', 
                   'interests_music', 'interests_movies', 'description']
        

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'percentage']
