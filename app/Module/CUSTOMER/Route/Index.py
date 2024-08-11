from Helper.utils import Enum


routes = [
    {
        "model": "CUSMST00",
        "applyRoutes": "all",
        "route": "/maintainpo",
       
    }
]

# Example usage
for route in routes:
    print(f"Route: {route['route']}, Model: {route['model']}")
