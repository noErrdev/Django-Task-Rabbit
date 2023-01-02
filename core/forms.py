from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='Email', required=True)
    password1 = forms.CharField(label='Password',
                                        widget=forms.PasswordInput, 
                                        min_length=8, 
                                        help_text="Your password can't be too similiar to your other personal information and be at least 8 characters")
    password2 = forms.CharField(label='Confirm password',
                                        widget=forms.PasswordInput, min_length=8, help_text="Enter the same password as before, for verification")
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'username', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email):
            raise ValidationError("Email already exists!")
        return email

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']