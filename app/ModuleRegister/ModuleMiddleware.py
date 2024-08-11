from django.utils.deprecation import MiddlewareMixin

class ModuleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Assuming moduleData and routeData are passed in the request attributes
        request.module_info = getattr(request, 'module_data', None)  # module install data
        request.route_data = getattr(request, 'route_data', None)    # module route data
