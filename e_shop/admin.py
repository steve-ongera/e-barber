from django.contrib import admin
from .models import Barber, ServiceCategory, Service, BusinessHours, Appointment, UserProfile, Review

@admin.register(Barber)
class BarberAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'years_of_experience')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone_number')
    list_filter = ('years_of_experience',)

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'duration', 'is_active')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'is_active')

@admin.register(BusinessHours)
class BusinessHoursAdmin(admin.ModelAdmin):
    list_display = ('day', 'opening_time', 'closing_time', 'is_closed')
    list_filter = ('is_closed',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'barber', 'service', 'date', 'start_time', 'status')
    search_fields = ('customer__username', 'barber__user__username', 'service__name')
    list_filter = ('status', 'date')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'phone_number')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'barber', 'service', 'rating', 'created_at')
    search_fields = ('customer__username', 'barber__user__username', 'service__name')
    list_filter = ('rating',)
