from django.db import models

class Taxi(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    vehicle_type = models.CharField(max_length=100)
    capacity = models.IntegerField()
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.vehicle_type}"
    
    class Meta:
        verbose_name_plural = "Taxis"


class Cottage(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=300)
    bedrooms = models.IntegerField()
    max_guests = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = models.TextField(help_text="Comma-separated amenities")
    image_url = models.URLField(blank=True, null=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.location}"


class Package(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    duration_days = models.IntegerField()
    destinations = models.TextField(help_text="Comma-separated destinations")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    includes = models.TextField(help_text="What's included in the package")
    image_url = models.URLField(blank=True, null=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.duration_days} days"


class Booking(models.Model):
    BOOKING_TYPES = [
        ('taxi', 'Taxi'),
        ('cottage', 'Cottage'),
        ('package', 'Package'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPES)
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    number_of_guests = models.IntegerField(default=1)
    special_requests = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    taxi = models.ForeignKey(Taxi, on_delete=models.SET_NULL, null=True, blank=True)
    cottage = models.ForeignKey(Cottage, on_delete=models.SET_NULL, null=True, blank=True)
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.booking_type.title()} Booking - {self.customer_name}"
    
    class Meta:
        ordering = ['-created_at']


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    class Meta:
        ordering = ['-created_at']

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-subscribed_at']
