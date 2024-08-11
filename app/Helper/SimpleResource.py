from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from django.db import transaction
from ..ModuleRegister.RegisterModel import registerModel
 

 # Adjust import as per your model's path
 # Adjust import for Redis functions
from ..Helper import getStatus, getPagination  # Adjust import as per your helper functions
import json

def generate_cache_key(request):
    cache_key = ''
    company = request.headers.get('company')
    whse = request.headers.get('whse')
    inowner = request.headers.get('inowner')
    page = request.headers.get('page')
    size = request.headers.get('size')
    langid = request.headers.get('langid')

    if company:
        cache_key += company
    if whse:
        cache_key += whse
    if inowner:
        cache_key += inowner
    cache_key += request.path
    if page:
        cache_key += page
    if size:
        cache_key += size
    if langid:
        cache_key += langid

    print("CACHE KEY ==========>", cache_key)
    return cache_key



class SimpleResourceView(View):

    async def get(self, request, *args, **kwargs):
        model_name = kwargs.get('model')
        resource_model = registerModel.getModel(model_name)

        # Generate cache key
        cache_key = generate_cache_key(request)
        

        
        # Proceed with fetching data from the database
        page = request.headers.get('page', 1)
        size = request.headers.get('size', 10)
        limit, offset = getPagination(page, size)

        # Add your filtering and querying logic here, similar to the original code
        # For example:
        filter_conditions = {
            'COMPANY': request.headers.get('company'),
            'WHSE': request.headers.get('whse'),
            'INOWNER': request.headers.get('inowner'),
        }

        # Fetch data from the database
        data = await resource_model.objects.filter(**filter_conditions)[offset:limit]

        # Store data in cache
        

        return JsonResponse({
            "status": 200,
            "message": "Data fetched successfully",
            "data": data,
        })

    async def post(self, request, *args, **kwargs):
        model_name = kwargs.get('model')
        resource_model = registerModel.getModel(model_name)

        # Deserialize JSON body
        req_data = json.loads(request.body)
        req_data['COMPANY'] = int(request.headers.get('company'))
        req_data['WHSE'] = int(request.headers.get('whse'))
        req_data['INOWNER'] = int(request.headers.get('inowner'))

        async with transaction.atomic():
            result = await resource_model.create(**req_data)

        return JsonResponse({
            "status": 200,
            "message": "Data created successfully",
            "data": result,
        })

    async def put(self, request, *args, **kwargs):
        model_name = kwargs.get('model')
        resource_model = registerModel.getModel(model_name)
        id = kwargs.get('id')
        req_data = json.loads(request.body)

        async with transaction.atomic():
            affected_rows = await resource_model.objects.filter(id=id).update(**req_data)

        if affected_rows:
            return JsonResponse({
                "status": 200,
                "message": "Data updated successfully",
                "data": req_data,
            })
        else:
            return JsonResponse({
                "status": 404,
                "message": "Id not found",
                "data": [],
            })

    async def delete(self, request, *args, **kwargs):
        model_name = kwargs.get('model')
        resource_model = registerModel.getModel(model_name)
        id = kwargs.get('id')

        async with transaction.atomic():
            affected_rows = await resource_model.objects.filter(id=id).delete()

        if affected_rows:
            return JsonResponse({
                "status": 200,
                "message": "Data deleted successfully",
                "data": [],
            })
        else:
            return JsonResponse({
                "status": 404,
                "message": "Id not found",
                "data": [],
            })
