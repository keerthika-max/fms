# helper/function.py
import os
import random
import asyncio
import aiohttp
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from your_module import registerModel  # Adjust the import as per your project structure

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("PGDB_URI")  # Use your actual database URL
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

class HelperFunctionController:
    def __init__(self):
        pass

    @staticmethod
    async def get_file_path(path):
        folder_name = "public"
        path = path.split(folder_name)
        return folder_name + path[1]

    @staticmethod
    def get_otp(id):
        val = random.randint(1000, 9999)
        with Session() as session:
            otp_array = session.execute(
                text("SELECT otp FROM OTP WHERE receiver = :receiver"), 
                {'receiver': id}
            ).fetchall()
        
        equal = lambda data: data.otp == val
        while any(equal(data) for data in otp_array):
            val = random.randint(1000, 9999)
        return val

    @staticmethod
    async def pagination_builder(query=""):
        pagination = {}
        take = query.get('_limit')
        page_no = query.get('_page', 1)
        skip = (page_no - 1) * take
        pagination['take'] = int(take)
        pagination['skip'] = int(skip)
        return pagination

    @staticmethod
    async def fixed_num(value):
        return round(value, 2)

    @staticmethod
    async def get_paging_data(data, page, limit):
        total_items = data.count()
        result = data.all()
        current_page = page or 0
        total_pages = (total_items + limit - 1) // limit  # Ceiling division
        return {"totalItems": total_items, "totalPages": total_pages, "currentPage": current_page, "result": result}

    @staticmethod
    async def get_fields(table_name):
        try:
            with Session() as session:
                table_columns = session.execute(
                    text(f"""
                    SELECT
                      c.column_name,
                      c.column_default,
                      c.is_nullable,
                      c.data_type,
                      c.udt_name,
                      c.character_maximum_length,
                      c.numeric_precision,
                      c.numeric_scale,
                      c.is_updatable,
                      CASE
                      WHEN tc.constraint_type = 'PRIMARY KEY' THEN 'Primary Key'
                      WHEN tc.constraint_type = 'UNIQUE' THEN 'Unique Key'
                      ELSE NULL
                      END AS constraint_type
                    FROM information_schema.columns c
                    LEFT JOIN information_schema.constraint_column_usage ccu ON c.column_name = ccu.column_name AND c.table_name = ccu.table_name
                    LEFT JOIN information_schema.table_constraints tc ON ccu.constraint_name = tc.constraint_name
                    WHERE c.table_name = :table_name
                    """),
                    {'table_name': table_name}
                ).fetchall()

                field_obj = {}
                for column in table_columns:
                    # Logic to determine data type and constraints
                    field_type = "String"  # Default
                    allow_null = column.is_nullable == "YES"
                    not_empty = column.is_nullable == "NO"

                    # Determine the field type based on `column.udt_name` or `column.data_type`
                    # Update field_obj accordingly
                    field_obj[column.column_name] = {
                        'type': field_type,
                        'allowNull': allow_null,
                    }
                    if not_empty:
                        field_obj[column.column_name]['validate'] = {'notEmpty': not_empty}
                    # Handle unique constraints similarly

                return field_obj
        except Exception as error:
            print(error)

    @staticmethod
    async def generate_serial_controll_number(req, url):
        try:
            headers = {
                'Authorization': req.headers['authorization'],
                'Company': req.headers['company'],
                'Whse': req.headers['whse'],
                'Inowner': req.headers['inowner'],
            }

            base_url = os.getenv('BASEURL')
            async with aiohttp.ClientSession() as session:
                async with session.put(f"{base_url}{url}", headers=headers) as response:
                    response_data = await response.json()
                    return response_data['data']
        except Exception as error:
            print(error)

    @staticmethod
    async def validate_vendor(vendor, company, whse, inowner):
        try:
            VNDMST00 = registerModel.get_model('VNDMST00')
            vendor_check = await VNDMST00.query.filter_by(COMPANY=company, INOWNER=inowner, VENDOR=vendor).first()
            return vendor_check is not None
        except Exception as error:
            print(error)
            return {"success": False, "data": str(error)}

    # Repeat similar methods for validate_customer, validate_gpnum, etc.

# Helper functions outside the class
def get_otp():
    return random.randint(1000, 9999)

def get_pagination(page, size):
    limit = size if size else 25
    offset = (page - 1) * limit if page > 1 else 0
    return {'limit': limit, 'offset': offset}

def get_paging_data(data, page, limit):
    total_items = data.count()
    result = data.all()
    current_page = page or 0
    total_pages = (total_items + limit - 1) // limit  # Ceiling division
    return {"totalItems": total_items, "totalPages": total_pages, "currentPage": current_page, "result": result}

async def get_status():
    # Logic for getting status
    pass  # Implement the logic similar to your JavaScript code

# Expose functions
helper_functions = {
    "get_otp": get_otp,
    "get_pagination": get_pagination,
    "get_paging_data": get_paging_data,
    "get_status": get_status,
}
