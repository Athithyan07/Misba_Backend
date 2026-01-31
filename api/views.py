from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags
import threading
import requests

def send_sms_async(phone_number, message):
    def send():
        try:
            # Using Fast2SMS (Free Tier/Wallet) or similar
            # If you don't have an API key, it will just log the attempt
            api_key = getattr(settings, 'SMS_API_KEY', None)
            if not api_key:
                print(f"DEBUG: SMS to {phone_number} skipped (No API Key). Message: {message}")
                return

            url = "https://www.fast2sms.com/dev/bulkV2"
            payload = {
                "message": message,
                "language": "english",
                "route": "q",
                "numbers": phone_number,
            }
            headers = {
                'authorization': api_key,
                'Content-Type': "application/x-www-form-urlencoded",
                'Cache-Control': "no-cache",
            }
            response = requests.post(url, data=payload, headers=headers)
            print(f"DEBUG: SMS sent to {phone_number}. Response: {response.text}")
        except Exception as e:
            print(f"DEBUG: SMS failed to {phone_number}: {str(e)}")

    thread = threading.Thread(target=send)
    thread.start()

def send_email_async(subject, text_content, html_content, recipient_list):
    def send():
        try:
            from_email = settings.DEFAULT_FROM_EMAIL
            print(f"DEBUG: Starting email send to {recipient_list} via {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
            mail = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
            mail.attach_alternative(html_content, "text/html")
            mail.send(fail_silently=False)
            print(f"DEBUG: Email sent successfully to {recipient_list}")
        except Exception as e:
            print(f"DEBUG: Async email failed to {recipient_list}: {str(e)}")
            import traceback
            print(f"DEBUG: Traceback: {traceback.format_exc()}")
    
    thread = threading.Thread(target=send)
    thread.start()

from .models import Taxi, Cottage, Package, Booking, Contact, Newsletter
from .serializers import TaxiSerializer, CottageSerializer, PackageSerializer, BookingSerializer, ContactSerializer, NewsletterSerializer
from .permissions import IsAuthenticatedOrReadOnly, IsAuthenticatedForBookingAndContact


class TaxiViewSet(viewsets.ModelViewSet):
    queryset = Taxi.objects.all()
    serializer_class = TaxiSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CottageViewSet(viewsets.ModelViewSet):
    queryset = Cottage.objects.all()
    serializer_class = CottageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedForBookingAndContact]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        # Email Theme Colors
        brand_dark = '#0B0D17'
        brand_accent = '#C5A059'
        brand_red = '#FF0000'
        text_white = '#FFFFFF'
        text_muted = '#A0A0A0'

        # 1. Prepare Admin Email (HTML)
        admin_subject = f'NEW {booking.booking_type.upper()} BOOKING REQUEST - {booking.customer_name.upper()}'
        
        admin_html_content = f"""
        <html>
            <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: {brand_dark}; color: {text_white};">
                <div style="max-width: 600px; margin: 0 auto; padding: 40px; border: 1px solid {brand_accent}33;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: {brand_accent}; font-size: 24px; letter-spacing: 2px; text-transform: uppercase; margin: 0;">
                            <span style="color: {brand_red};">MISBA</span> TOURISM
                        </h1>
                        <p style="color: {text_muted}; font-size: 12px; letter-spacing: 4px; text-transform: uppercase; margin-top: 10px;">Admin Notification</p>
                    </div>
                    
                    <div style="background-color: rgba(197, 160, 89, 0.05); padding: 30px; border-radius: 15px; border-left: 4px solid {brand_accent};">
                        <h2 style="color: {brand_accent}; font-size: 18px; margin-top: 0; border-bottom: 1px solid {brand_accent}33; padding-bottom: 15px; font-weight: bold;">
                            NEW BOOKING DETAILS
                        </h2>
                        
                        <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                            <tr><td style="padding: 10px 0; color: {text_muted}; width: 150px;">Booking Type:</td><td style="padding: 10px 0; color: {text_white}; font-weight: bold; text-transform: capitalize;">{booking.booking_type}</td></tr>
                            <tr><td style="padding: 10px 0; color: {text_muted};">Customer:</td><td style="padding: 10px 0; color: {text_white}; font-weight: bold;">{booking.customer_name}</td></tr>
                            <tr><td style="padding: 10px 0; color: {text_muted};">Email:</td><td style="padding: 10px 0; color: {text_white}; font-weight: bold;">{booking.customer_email}</td></tr>
                            <tr><td style="padding: 10px 0; color: {text_muted};">Phone:</td><td style="padding: 10px 0; color: {text_white}; font-weight: bold;">{booking.customer_phone}</td></tr>
                            <tr><td style="padding: 10px 0; color: {text_muted};">Start Date:</td><td style="padding: 10px 0; color: {text_white}; font-weight: bold;">{booking.start_date}</td></tr>
                            <tr><td style="padding: 10px 0; color: {text_muted};">End Date:</td><td style="padding: 10px 0; color: {text_white}; font-weight: bold;">{booking.end_date or 'N/A'}</td></tr>
                            <tr><td style="padding: 10px 0; color: {text_muted};">Guests:</td><td style="padding: 10px 0; color: {text_white}; font-weight: bold;">{booking.number_of_guests}</td></tr>
                        </table>
                        
                        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid {brand_accent}33;">
                            <h3 style="color: {brand_accent}; font-size: 14px; margin-bottom: 10px;">SPECIAL REQUESTS:</h3>
                            <p style="color: {text_white}; font-style: italic; background: rgba(255,255,255,0.03); padding: 15px; border-radius: 8px;">
                                {booking.special_requests or 'No special requests provided.'}
                            </p>
                        </div>
                    </div>
                    
                    <div style="text-align: center; margin-top: 40px; color: {text_muted}; font-size: 12px;">
                        <p>This is an automated notification from your booking system.</p>
                        <p>&copy; 2026 Misba Tourism. All rights reserved.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        admin_text_content = strip_tags(admin_html_content)

        # 2. Prepare Customer Email (HTML)
        customer_subject = 'BOOKING RECEIVED - MISBA TOURISM'
        
        customer_html_content = f"""
        <html>
            <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: {brand_dark}; color: {text_white};">
                <div style="max-width: 600px; margin: 0 auto; padding: 40px; border: 1px solid {brand_accent}33;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: {brand_accent}; font-size: 24px; letter-spacing: 2px; text-transform: uppercase; margin: 0;">
                            <span style="color: {brand_red};">MISBA</span> TOURISM
                        </h1>
                        <p style="color: {text_muted}; font-size: 10px; letter-spacing: 3px; text-transform: uppercase; margin-top: 10px;">Premium Travel Experiences</p>
                    </div>
                    
                    <div style="text-align: center; padding: 40px 20px; background: linear-gradient(135deg, {brand_dark} 0%, #1a1d2e 100%); border-radius: 20px; border: 1px solid {brand_accent}22;">
                        <h2 style="color: {brand_accent}; font-size: 28px; font-serif: 'Playfair Display', serif; margin-bottom: 20px; font-weight: bold;">
                            THANK YOU, {booking.customer_name.split()[0].upper()}!
                        </h2>
                        <p style="color: {text_white}; font-size: 16px; line-height: 1.6; margin-bottom: 30px;">
                            We have received your request for a <strong>{booking.booking_type}</strong>. 
                            Our concierge team is currently reviewing your details and will contact you within 24 hours to finalize your reservation.
                        </p>
                        
                        <div style="display: inline-block; padding: 15px 30px; border: 1px solid {brand_accent}; color: {brand_accent}; text-transform: uppercase; letter-spacing: 2px; font-size: 12px; font-weight: bold; border-radius: 5px;">
                            Request Status: Pending Confirmation
                        </div>
                    </div>
                    
                    <div style="margin-top: 40px; padding-top: 30px; border-top: 1px solid {brand_accent}33; text-align: center;">
                        <p style="color: {text_muted}; font-size: 14px; margin-bottom: 20px;">Follow our journey</p>
                        <div style="margin-bottom: 30px;">
                            <a href="#" style="color: {brand_accent}; text-decoration: none; margin: 0 10px;">Instagram</a>
                            <a href="#" style="color: {brand_accent}; text-decoration: none; margin: 0 10px;">Facebook</a>
                            <a href="#" style="color: {brand_accent}; text-decoration: none; margin: 0 10px;">Twitter</a>
                        </div>
                        <p style="color: {text_muted}; font-size: 11px;">
                            If you have any urgent questions, please reply to this email or call us at +91 63838 55638 / +91 63831 69699.
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """
        customer_text_content = strip_tags(customer_html_content)

        # Send Emails in Background
        print(f"Triggering background notifications for booking: {booking.id}")
        
        # 1. Background Emails
        send_email_async(
            customer_subject,
            customer_text_content,
            customer_html_content,
            [booking.customer_email]
        )
        send_email_async(
            admin_subject,
            admin_text_content,
            admin_html_content,
            [settings.ADMIN_EMAIL]
        )
        
        # 2. Background SMS Notifications
        admin_sms_msg = f"NEW BOOKING: {booking.booking_type.upper()} from {booking.customer_name} ({booking.customer_phone}). Date: {booking.start_date}"
        customer_sms_msg = f"Hi {booking.customer_name}, your booking request for {booking.booking_type} has been received by Misba Tourism. We will contact you shortly."
        
        # Send to Admin
        send_sms_async(settings.ADMIN_PHONE, admin_sms_msg)
        
        # Send to Customer (only if valid phone exists)
        if booking.customer_phone:
            send_sms_async(booking.customer_phone, customer_sms_msg)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticatedForBookingAndContact]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = serializer.save()

        # Email Theme Colors
        brand_dark = '#0B0D17'
        brand_accent = '#C5A059'
        brand_red = '#FF0000'
        text_white = '#FFFFFF'
        text_muted = '#A0A0A0'

        # 1. Admin Email
        admin_subject = f'NEW CONTACT INQUIRY - {contact.name.upper()}'
        admin_html = f"""
        <html>
            <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: {brand_dark}; color: {text_white};">
                <div style="max-width: 600px; margin: 0 auto; padding: 40px; border: 1px solid {brand_accent}33;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: {brand_accent}; font-size: 24px; letter-spacing: 2px; text-transform: uppercase; margin: 0;">
                            <span style="color: {brand_red};">MISBA</span> TOURISM
                        </h1>
                        <p style="color: {text_muted}; font-size: 12px; letter-spacing: 4px; text-transform: uppercase; margin-top: 10px;">Contact Request</p>
                    </div>
                    
                    <div style="background-color: rgba(197, 160, 89, 0.05); padding: 30px; border-radius: 15px; border-left: 4px solid {brand_accent};">
                        <h2 style="color: {brand_accent}; font-size: 18px; margin-top: 0; border-bottom: 1px solid {brand_accent}33; padding-bottom: 15px; font-weight: bold;">
                            INQUIRY DETAILS
                        </h2>
                        
                        <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                            <tr><td style="padding: 10px 0; color: {text_muted}; width: 150px;">Name:</td><td style="padding: 10px 0; color: {text_white}; font-weight: bold;">{contact.name}</td></tr>
                            <tr><td style="padding: 10px 0; color: {text_muted};">Email:</td><td style="padding: 10px 0; color: {text_white}; font-weight: bold;">{contact.email}</td></tr>
                            <tr><td style="padding: 10px 0; color: {text_muted};">Phone:</td><td style="padding: 10px 0; color: {text_white}; font-weight: bold;">{contact.phone or 'N/A'}</td></tr>
                            <tr><td style="padding: 10px 0; color: {text_muted};">Subject:</td><td style="padding: 10px 0; color: {text_white}; font-weight: bold;">{contact.subject}</td></tr>
                        </table>
                        
                        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid {brand_accent}33;">
                            <h3 style="color: {brand_accent}; font-size: 14px; margin-bottom: 10px;">MESSAGE:</h3>
                            <p style="color: {text_white}; background: rgba(255,255,255,0.03); padding: 15px; border-radius: 8px; line-height: 1.6;">
                                {contact.message}
                            </p>
                        </div>
                    </div>
                    
                    <div style="text-align: center; margin-top: 40px; color: {text_muted}; font-size: 12px;">
                        <p>&copy; 2026 Misba Tourism. All rights reserved.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # 2. Customer Email
        customer_subject = 'WE HAVE RECEIVED YOUR MESSAGE - MISBA TOURISM'
        customer_html = f"""
        <html>
            <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: {brand_dark}; color: {text_white};">
                <div style="max-width: 600px; margin: 0 auto; padding: 40px; border: 1px solid {brand_accent}33;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: {brand_accent}; font-size: 24px; letter-spacing: 2px; text-transform: uppercase; margin: 0;">
                            <span style="color: {brand_red};">MISBA</span> TOURISM
                        </h1>
                    </div>
                    
                    <div style="text-align: center; padding: 40px 20px; background: rgba(197, 160, 89, 0.03); border-radius: 20px;">
                        <h2 style="color: {brand_accent}; font-size: 24px; margin-bottom: 20px; font-weight: bold;">HELLO {contact.name.split()[0].upper()},</h2>
                        <p style="color: {text_white}; font-size: 16px; line-height: 1.6; margin-bottom: 30px;">
                            Thank you for reaching out to Misba Tourism. We have received your message regarding <strong>"{contact.subject}"</strong>.
                            Our team will get back to you as soon as possible.
                        </p>
                    </div>
                    
                    <div style="margin-top: 40px; text-align: center; color: {text_muted}; font-size: 11px;">
                        <p>Misba Tourism - Premium Travel Experiences</p>
                        <p style="margin-top: 10px;">For urgent inquiries: +91 63838 55638 / +91 63831 69699</p>
                    </div>
                </div>
            </body>
        </html>
        """

        # Send Emails in Background
        print(f"Triggering background notifications for contact inquiry: {contact.id}")
        
        # 1. Background Emails
        send_email_async(
            admin_subject,
            strip_tags(admin_html),
            admin_html,
            [settings.ADMIN_EMAIL]
        )
        send_email_async(
            customer_subject,
            strip_tags(customer_html),
            customer_html,
            [contact.email]
        )

        # 2. Background SMS Notification
        admin_sms_msg = f"NEW INQUIRY: {contact.name} ({contact.phone}). Subject: {contact.subject}"
        send_sms_async(settings.ADMIN_PHONE, admin_sms_msg)
        
        if contact.phone:
            customer_sms_msg = f"Hi {contact.name}, thank you for contacting Misba Tourism. We have received your message and will respond shortly."
            send_sms_async(contact.phone, customer_sms_msg)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if already subscribed
        if Newsletter.objects.filter(email=email).exists():
            return Response({"message": "You are already subscribed to our newsletter!"}, status=status.HTTP_200_OK)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Send confirmation email in background
        send_email_async(
            'Welcome to Misba Tourism Newsletter!',
            'Thank you for subscribing to our newsletter. You will now receive exclusive updates and hidden gems directly to your inbox.',
            '<h1>Welcome!</h1><p>Thank you for subscribing to our newsletter. You will now receive exclusive updates and hidden gems directly to your inbox.</p>',
            [email]
        )

        return Response({"message": "Successfully subscribed to our newsletter!"}, status=status.HTTP_201_CREATED)
