from django.db import models
from app.Helper.function import HelperFunctionController as helper

class CUSMST00(models.Model):
    __tablename__ = 'CUSMST00'

    # Fetching the fields using a helper function
    field_obj = helper.get_fields(__tablename__)

    # Dynamically defining fields based on field_obj
    for field in field_obj:
        field_type = field['type']
        field_name = field['name']
        primary_key = field.get('primary_key', False)

        # Use Django's model field types
        if field_type == 'IntegerField':
            vars()[field_name] = models.IntegerField(primary_key=primary_key)
        elif field_type == 'CharField':
            vars()[field_name] = models.CharField(max_length=field.get('max_length', 255), primary_key=primary_key)
        # Add other field types as necessary, e.g., models.BooleanField, models.DateField, etc.

    class Meta:
        db_table = 'CUSMST00'  # Specify the table name in PostgreSQL
        indexes = [
            models.Index(fields=['id'], name='primary_key_index', unique=True),
        ]
