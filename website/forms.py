from django import forms
from .models import UserProfile, UserPostModel

class SignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = UserProfile
        fields = "__all__"
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data
    
class UserPostForm(forms.ModelForm):
    class Meta:
        model = UserPostModel
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super().__init__(*args, **kwargs)

        if user_profile:
            self.fields['user_profile'].initial = user_profile
            self.fields['user_profile'].widget = forms.HiddenInput() 
            # You can also set a display label if needed
            self.fields['user_profile'].label = f"{user_profile.first_name} {user_profile.last_name}"
