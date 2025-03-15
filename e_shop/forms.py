from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Appointment, UserProfile, Review

class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone_number', 'profile_picture')

class AppointmentForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Select a date for your appointment"
    )
    start_time = forms.TimeField(
        widget=forms.Select(choices=[]),
        help_text="Select an available time slot"
    )
    
    class Meta:
        model = Appointment
        fields = ('service', 'barber', 'date', 'start_time', 'notes')
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any special requests or notes?'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Time choices will be populated via JavaScript based on selected date and barber

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your experience'})
        }