from django.contrib import admin
from .models import Barber, ServiceCategory, Service, BusinessHours, Appointment,  Review , Profile

@admin.register(Barber)
class BarberAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'years_of_experience')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone_number')
    list_filter = ('years_of_experience',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address','city')
    search_fields = ('user__username', 'phone')



@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

from django.contrib import admin
from .models import Service, SubService

class SubServiceInline(admin.TabularInline):  # You can also use StackedInline if you prefer
    model = SubService
    extra = 1  # Number of empty forms shown


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'duration', 'is_active')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'is_active')
    inlines = [SubServiceInline]  # Add this line to include SubServices



@admin.register(BusinessHours)
class BusinessHoursAdmin(admin.ModelAdmin):
    list_display = ('day', 'opening_time', 'closing_time', 'is_closed')
    list_filter = ('is_closed',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'barber', 'service', 'date', 'start_time', 'status')
    search_fields = ('customer__username', 'barber__user__username', 'service__name')
    list_filter = ('status', 'date')



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'barber', 'service', 'rating', 'created_at')
    search_fields = ('customer__username', 'barber__user__username', 'service__name')
    list_filter = ('rating',)
