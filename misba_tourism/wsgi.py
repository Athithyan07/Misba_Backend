"""
WSGI config for misba_tourism project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import django
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'misba_tourism.settings')
django.setup()

# Force migrations on startup
try:
    print("Running force migrations from wsgi.py...")
    call_command('migrate', interactive=False)
    print("Migrations completed successfully!")
except Exception as e:
    print(f"Migration error in wsgi.py: {e}")

application = get_wsgi_application()
