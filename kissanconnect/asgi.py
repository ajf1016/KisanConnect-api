import os
from django.core.asgi import get_asgi_application
import django
django.setup()


# ----


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kissanconnect.settings')

application = get_asgi_application()
