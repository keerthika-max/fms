# constants.py

class Constants:
    user_role = {
        'ADMIN': 'ADMIN',
        'VENDOR': 'VENDOR',
        'CUSTOMER': 'CUSTOMER',
    }
    auth = {
        'cipher_key': 'wms-auth-key',
    }
    admin_code = 'ADMIN001'
    verified_status = 'verified'
    not_verified_status = 'notverified'
    verification_for = {
        'user_phone': 'userPhone',
        'provider_phone': 'providerPhone',
        'delivery_phone': 'deliveryBoyPhone',
    }

# Optionally, you can create an instance of Constants if needed
constants = Constants()
