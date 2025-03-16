from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Service, ServiceCategory, Barber, Appointment, BusinessHours
from .forms import AppointmentForm, UserProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User

def home(request):
    """Home page view"""
    services = ServiceCategory.objects.all()
    barbers = Barber.objects.all()
    context = {
        'services': services,
        'barbers': barbers,
    }
    return render(request, 'home.html', context)




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    messages.error(request, "Logged out successfully!")
    return redirect('home')

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegistrationForm

def signup(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')  # Redirect to your home page
        else:
            # Add form errors as messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()
    
    return render(request,  'registration/signup.html', {"form": form})

def category_detail(request, slug):
    """View showing services in a specific category"""
    category = get_object_or_404(ServiceCategory, slug=slug)
    services = Service.objects.filter(category=category, is_active=True)
    return render(request, 'category_detail.html', {
        'category': category,
        'services': services
    })


def service_list(request):
    """View all services offered by the barber shop"""
    categories = ServiceCategory.objects.all()
    return render(request, 'service_list.html', {'categories': categories})

def service_detail(request, slug):
    """View details of a specific service"""
    service = get_object_or_404(Service, slug=slug)
    return render(request, 'service_detail.html', {'service': service})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from .models import Service, Appointment, Barber
from .forms import AppointmentForm

from datetime import timedelta, datetime

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from datetime import datetime, timedelta
from .models import Appointment, Service
from .forms import AppointmentForm
from datetime import datetime, timedelta, time
from django.core.exceptions import ValidationError
from datetime import timedelta, datetime

@login_required
def book_appointment(request, slug):
    """Allow a logged-in user to book an appointment for a service."""
    service = get_object_or_404(Service, slug=slug)
    
    # Debug information
    print(f"Service found: {service.id} - {service.name}")

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        
        # Debug form data
        print(f"POST data: {request.POST}")
        
        if form.is_valid():
            # Debug cleaned data
            print(f"Form cleaned data: {form.cleaned_data}")
            
            try:
                appointment = form.save(commit=False)
                
                # Explicitly check all required fields
                if not form.cleaned_data.get('barber'):
                    form.add_error('barber', 'Barber is required')
                    raise ValidationError('Barber is required')
                
                appointment.customer = request.user
                appointment.service = service
                appointment.amount = service.price
                
                # Set end_time before saving
                start_datetime = datetime.combine(appointment.date, appointment.start_time)
                end_datetime = start_datetime + timedelta(hours=1)
                appointment.end_time = end_datetime.time()
                
                # Debug the appointment object before saving
                print(f"About to save appointment: Customer: {appointment.customer}, Service: {appointment.service}, Barber: {appointment.barber}")
                
                appointment.save()
                messages.success(request, f"Appointment for {service.name} booked successfully!")
                return redirect('appointment_success')
            except Exception as e:
                print(f"Exception occurred: {str(e)}")
                form.add_error(None, f"Error saving appointment: {str(e)}")
        else:
            # Form validation failed
            print(f"Form validation errors: {form.errors}")
    else:
        form = AppointmentForm(initial={
            'customer_name': request.user.get_full_name(),
            'customer_email': request.user.email,
        })

    return render(request, 'book_appointment.html', {'form': form, 'service': service})





@login_required
def appointment_detail(request, appointment_id):
    """View details of a specific appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id, customer=request.user)
    return render(request, 'appointment_detail.html', {'appointment': appointment})

@login_required
def my_appointments(request):
    """View all appointments for the logged-in user"""
    appointments = Appointment.objects.filter(customer=request.user).order_by('date', 'start_time')
    return render(request, 'my_appointments.html', {'appointments': appointments})

def get_available_slots(request):
    """API endpoint to get available time slots for a specific date and barber"""
    if request.method == 'GET':
        date_str = request.GET.get('date')
        barber_id = request.GET.get('barber_id')
        service_id = request.GET.get('service_id')
        
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            barber = Barber.objects.get(id=barber_id)
            service = Service.objects.get(id=service_id)
            
            # Get business hours for the day
            day_of_week = selected_date.weekday()
            try:
                business_hours = BusinessHours.objects.get(day=day_of_week)
                if business_hours.is_closed:
                    return JsonResponse({'available_slots': [], 'message': 'Closed on this day'})
            except BusinessHours.DoesNotExist:
                return JsonResponse({'available_slots': [], 'message': 'No business hours defined for this day'})
            
            # Generate all possible time slots
            slots = []
            current_time = business_hours.opening_time
            closing_time = business_hours.closing_time
            service_duration = timedelta(minutes=service.duration)
            
            while (datetime.combine(selected_date, current_time) + service_duration).time() <= closing_time:
                # Check if slot is available (not booked)
                existing_appointments = Appointment.objects.filter(
                    barber=barber,
                    date=selected_date,
                    status='scheduled'
                ).filter(
                    # Check if the slot overlaps with any existing appointment
                    start_time__lt=(datetime.combine(selected_date, current_time) + service_duration).time(),
                    end_time__gt=current_time
                )
                
                if not existing_appointments:
                    slots.append(current_time.strftime('%I:%M %p'))
                
                # Move to next slot (30 min intervals)
                current_time = (datetime.combine(selected_date, current_time) + timedelta(minutes=30)).time()
            
            return JsonResponse({'available_slots': slots})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)