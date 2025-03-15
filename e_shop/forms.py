from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Appointment, UserProfile, Review
from datetime import datetime, date, timedelta
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class UserRegistrationForm(forms.ModelForm):
    """Custom registration form that allows simple passwords"""
    
    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Choose any password you'd like."
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Enter the same password again for verification."
    )
    
    class Meta:
        model = User
        fields = ["username", "email"]
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email address already exists.")
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if not password1 or not password2:
            raise ValidationError("Please enter a password and confirm it.")
        
        if password1 != password2:
            raise ValidationError("The two password fields didn't match.")
        
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone_number', 'profile_picture')

    
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['customer_name', 'customer_email', 'customer_address', 'date', 'start_time', 'barber', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'barber': forms.Select(attrs={'class': 'form-control'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'customer_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        date = cleaned_data.get('date')
        
        if start_time and date:
            # Set end_time to be 1 hour after start_time
            start_datetime = datetime.combine(date, start_time)
            end_datetime = start_datetime + timedelta(hours=1)
            cleaned_data['end_time'] = end_datetime.time()
        
        return cleaned_data


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your experience'})
        }