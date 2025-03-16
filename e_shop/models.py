from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Barber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='barbers/', blank=True, null=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

from django.db import models
from django.utils.text import slugify

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, blank=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug only if it's empty
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Service Categories"


class Service(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name="services")
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug only if it's empty
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (ksh{self.price})"

    class Meta:
        verbose_name_plural = "Services"

class BusinessHours(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    day = models.IntegerField(choices=DAYS_OF_WEEK)
    opening_time = models.TimeField(null=True, blank=True)  # Allow NULL values
    closing_time = models.TimeField(null=True, blank=True)  # Allow NULL values
    is_closed = models.BooleanField(default=False)
    
    def __str__(self):
        if self.is_closed:
            return f"{self.get_day_display()}: Closed"
        return f"{self.get_day_display()}: {self.opening_time.strftime('%I:%M %p')} - {self.closing_time.strftime('%I:%M %p')}"
    
    class Meta:
        verbose_name_plural = "Business Hours"
        ordering = ['day']

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import time
from e_shop.models import Service, Barber

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name="appointments")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    # New Fields
    amount = models.DecimalField(max_digits=6, decimal_places=2, blank=True , null=True)  
    customer_email = models.EmailField(blank=True , null=True)
    customer_name = models.CharField(max_length=255 , blank=True , null=True)
    customer_address = models.TextField(blank=True , null=True)

    def __str__(self):
        return f"{self.customer_name} - {self.service.name} - {self.date} {self.start_time}"


    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ('barber', 'date', 'start_time')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.user.username

class Review(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    barber = models.ForeignKey(Barber, on_delete=models.SET_NULL, null=True, related_name="reviews")
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.customer.username} - {self.rating} stars"