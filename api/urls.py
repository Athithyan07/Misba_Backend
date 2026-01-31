from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaxiViewSet, CottageViewSet, PackageViewSet, BookingViewSet, ContactViewSet, NewsletterViewSet

router = DefaultRouter()
router.register(r'taxis', TaxiViewSet)
router.register(r'cottages', CottageViewSet)
router.register(r'packages', PackageViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'newsletters', NewsletterViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
