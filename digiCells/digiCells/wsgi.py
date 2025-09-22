"""
WSGI config for digiCells project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from django.core.wsgi import get_wsgi_application

# Set the Django settings module based on environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digiCells.digiCells.settings.production')

application = get_wsgi_application()
