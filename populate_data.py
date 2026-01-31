import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'misba_tourism.settings')
django.setup()

from api.models import Taxi, Cottage, Package

print("Populating database with sample data...")

taxis = [
    {
        'name': 'Luxury Sedan',
        'description': 'Comfortable luxury sedan for your premium travel needs',
        'vehicle_type': 'Sedan',
        'capacity': 4,
        'price_per_km': 2.50,
        'available': True,
    },
    {
        'name': 'Family SUV',
        'description': 'Spacious SUV perfect for family trips',
        'vehicle_type': 'SUV',
        'capacity': 7,
        'price_per_km': 3.50,
        'available': True,
    },
    {
        'name': 'Executive Van',
        'description': 'Large van for group transportation',
        'vehicle_type': 'Van',
        'capacity': 12,
        'price_per_km': 4.50,
        'available': True,
    },
]

cottages = [
    {
        'name': 'Mountain View Cottage',
        'description': 'Beautiful cottage with stunning mountain views',
        'location': 'Mountain Valley',
        'bedrooms': 3,
        'max_guests': 6,
        'price_per_night': 150.00,
        'amenities': 'WiFi, Fireplace, Kitchen, Parking, Hot Tub',
        'available': True,
    },
    {
        'name': 'Lakeside Retreat',
        'description': 'Peaceful cottage by the lake with private dock',
        'location': 'Crystal Lake',
        'bedrooms': 2,
        'max_guests': 4,
        'price_per_night': 120.00,
        'amenities': 'WiFi, BBQ, Kayaks, Fishing Gear, Deck',
        'available': True,
    },
    {
        'name': 'Forest Hideaway',
        'description': 'Cozy cottage nestled in the forest',
        'location': 'Pine Forest',
        'bedrooms': 4,
        'max_guests': 8,
        'price_per_night': 200.00,
        'amenities': 'WiFi, Fireplace, Game Room, Sauna, Hiking Trails',
        'available': True,
    },
]

packages = [
    {
        'name': 'Weekend Getaway',
        'description': 'Perfect 2-day escape from the city',
        'duration_days': 2,
        'destinations': 'Mountain Valley, Crystal Lake',
        'price': 299.00,
        'includes': 'Accommodation, Transportation, Breakfast, Guided Tours',
        'available': True,
    },
    {
        'name': 'Adventure Week',
        'description': 'Full week of outdoor adventures and exploration',
        'duration_days': 7,
        'destinations': 'Mountain Valley, Pine Forest, Crystal Lake, Sunset Beach',
        'price': 1299.00,
        'includes': 'Accommodation, All Meals, Transportation, Adventure Activities, Tour Guide',
        'available': True,
    },
    {
        'name': 'Romantic Escape',
        'description': '3-day romantic getaway for couples',
        'duration_days': 3,
        'destinations': 'Sunset Beach, Crystal Lake',
        'price': 599.00,
        'includes': 'Luxury Accommodation, Candlelit Dinners, Spa Services, Private Tours',
        'available': True,
    },
]

for taxi_data in taxis:
    Taxi.objects.get_or_create(name=taxi_data['name'], defaults=taxi_data)
    print(f"Created taxi: {taxi_data['name']}")

for cottage_data in cottages:
    Cottage.objects.get_or_create(name=cottage_data['name'], defaults=cottage_data)
    print(f"Created cottage: {cottage_data['name']}")

for package_data in packages:
    Package.objects.get_or_create(name=package_data['name'], defaults=package_data)
    print(f"Created package: {package_data['name']}")

print("\nDatabase populated successfully!")
print(f"Total Taxis: {Taxi.objects.count()}")
print(f"Total Cottages: {Cottage.objects.count()}")
print(f"Total Packages: {Package.objects.count()}")
