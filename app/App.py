# App.py
import os
from pathlib import Path
from dotenv import load_dotenv
from django.core.asgi import get_asgi_application
from django.core.wsgi import get_wsgi_application
from django.http import JsonResponse
from django.urls import path
from django.conf import settings
from django.middleware.common import CommonMiddleware
from django.middleware.csrf import CsrfViewMiddleware
from django.utils.deprecation import MiddlewareMixin
from django.core.management import execute_from_command_line

BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file
load_dotenv(dotenv_path=BASE_DIR / ".env")

# Settings equivalent
# if not settings.configured:
if not settings.configured:
 settings.configure(
    SECRET_KEY=os.getenv('SECRET_KEY', 'default-secret-key'),
    DEBUG=os.getenv('DEBUG', 'True') == 'True',
    ALLOWED_HOSTS=['*'],
    ROOT_URLCONF=__name__,
    MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'App.CORSMiddleware',  # Custom middleware for CORS
    ],
    TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Add paths to your templates directory here if needed
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
],
    INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',  # Required
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'App',  # Include your app
        ],
    STATIC_URL='/public/',
    STATICFILES_DIRS=[BASE_DIR / "public"],
    TIME_ZONE=os.getenv('TIME_ZONE', 'Asia/Kolkata'),
    USE_TZ=True,
)
# settings.configured = True  

# Custom middleware for CORS
class CORSMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'OPTIONS,GET,PUT,POST,DELETE'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization,company,whse,inowner'
        response['Access-Control-Expose-Headers'] = 'x-total-count'
        if request.method == 'OPTIONS':
            response.status_code = 200
        return response

# Example view for user routes
def user_list(request):
    return JsonResponse({'users': [{'id': 1, 'name': 'John Doe'}]})

# URL configuration
urlpatterns = [
    path('user/', user_list),
]

# Entry point for the application
if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', __name__)
    application = get_wsgi_application() if os.getenv('USE_ASGI', 'False') == 'False' else get_asgi_application()
    execute_from_command_line(['manage.py', 'runserver'])
