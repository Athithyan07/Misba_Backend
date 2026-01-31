from django.contrib import admin
from .models import Taxi, Cottage, Package, Booking, Contact


@admin.register(Taxi)
class TaxiAdmin(admin.ModelAdmin):
    list_display = ('name', 'vehicle_type', 'capacity', 'price_per_km', 'available', 'created_at')
    list_filter = ('available', 'vehicle_type')
    search_fields = ('name', 'vehicle_type')


@admin.register(Cottage)
class CottageAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'bedrooms', 'max_guests', 'price_per_night', 'available', 'created_at')
    list_filter = ('available', 'location')
    search_fields = ('name', 'location')


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_days', 'price', 'available', 'created_at')
    list_filter = ('available', 'duration_days')
    search_fields = ('name', 'destinations')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'booking_type', 'start_date', 'status', 'created_at')
    list_filter = ('booking_type', 'status', 'start_date')
    search_fields = ('customer_name', 'customer_email', 'customer_phone')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject')
