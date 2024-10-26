from django import forms
from .models import UserInformation

class UserInformationForm(forms.ModelForm):
    class Meta:
        model = UserInformation
        fields = ['student_id', 'passout_year', 'profession', 'college', 
                  'birthday', 'country', 'state', 'city', 'languages', 
                  'email', 'phone', 'interests_music', 'interests_movies']
        
   