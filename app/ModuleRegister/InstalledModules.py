 # Adjust import based on your project structure
from Helper.utils import Enum


INSTALLED_MODULES = [
   
    {
        "name": "CUSTOMER",
        "type": "CUSTOMER",
        "include": ["model", "coreRoutes"],
        "description": "CUSTOMER",
        "appendMiddleware": [],
    },
]

# Optionally, you can define a function to get the installed modules if needed
def get_installed_modules():
    return INSTALLED_MODULES
