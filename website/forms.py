from django import forms
from .models import UserProfile

class SignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'password', 'confirm_password', 'college', 'current_status',
            'employee_id', 'student_id', 'passout_year'
        ]
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
