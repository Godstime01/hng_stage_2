import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hng_stage_2.settings')

application = get_wsgi_application()
# add this vercel variable
app = application
