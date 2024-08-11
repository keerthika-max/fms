import os
from pathlib import Path
from django.conf import settings
from django.urls import path, include
from django.core.management import call_command
from ..ModuleRegister import register_module, register_model, register_middleware
#import applyRoutes from "#wms/Helper/simpleResource";
from ..Helper import apply_routes
# Ensure Django is set up correctly
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
import django
django.setup()

# Define the base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Function to get middlewares
def get_middlewares(middleware):
    middlewares = []
    if middleware and isinstance(middleware, list):
        for mw in middleware:
            module = register_middleware.get(mw['name'])
            if module:
                if 'params' in mw:
                    middlewares.append(module['func'](*mw['params']))
                else:
                    middlewares.append(module['func'])
    return middlewares

# Load installed modules
installed_modules = register_module.get_installed_modules()
module_dir = BASE_DIR / "Module"

# Register core models
for item in installed_modules:
    print(item)
    folder_name = item['name']
    if 'model' in item.get('include', []):
        models_path = module_dir / folder_name / "Model" / "index.py"
        models_export = __import__(str(models_path).replace('/', '.'), fromlist=[''])
        models = models_export.models  # Adjust based on your actual export
        for model_data in models:
            register_model.register(model_data)

# After schema is changed from all models, then finally install the models
register_model.install()
register_model.list()

# Register middlewares
for item in installed_modules:
    folder_name = item['name']
    if 'middleware' in item.get('include', []):
        middleware_path = module_dir / folder_name / "Middleware" / "index.py"
        __import__(str(middleware_path).replace('/', '.'), fromlist=[''])

# List installed middlewares
register_middleware.list()

# Register routes
urlpatterns = []
for item in installed_modules:
    folder_name = item['name']
    if 'coreRoutes' in item.get('include', []):
        route_item_path = module_dir / folder_name / "Route" / "index.py"
        route_item = __import__(str(route_item_path).replace('/', '.'), fromlist=[''])
        route_data = route_item.routes  # Adjust based on your actual export

        for controller_file, routes in route_data.items():
            if isinstance(routes, list):
                if controller_file != 'ResourceRoutes':
                    controller_item_path = module_dir / folder_name / "Controller" / f"{controller_file}.py"
                    controller_item = __import__(str(controller_item_path).replace('/', '.'), fromlist=[''])
                    controller = controller_item.controller  # Adjust based on your actual export

                    for route in routes:
                        middlewares = get_middlewares(route.get('middleware', []))
                        after_control_middlewares = get_middlewares(route.get('aftercontrlmiddleware', []))
                        print("ch", route['method'], route['action'])

                        urlpatterns.append(
                            path(route['route'], 
                                 *middlewares + [getattr(controller, route['action'])] + after_control_middlewares)
                        )
                else:
                    # Handle resource routes
                    resource_routes = route_data[controller_file]
                    for el in resource_routes:
                        el['middlewares'] = get_middlewares(el.get('middlewares', []))
                        apply_routes(item, el)  # Define apply_routes separately

            else:
                # Handle single route
                cont_mid = routes
                cont_mid['middlewares'] = get_middlewares(cont_mid.get('middlewares', []))
                apply_routes(item, cont_mid)  # Define apply_routes separately

# Register the URLs in your Django project's main urls.py
urlpatterns = [
    path('api/', include((urlpatterns, 'api'), namespace='api')),  # Use your desired namespace
]

# Make sure to call migrations and other startup commands
call_command('migrate')
