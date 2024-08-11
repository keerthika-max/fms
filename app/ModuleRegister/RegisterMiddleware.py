class MiddlewareRegister:
    def __init__(self):
        self._map = {}

    def list(self):
        for key, value in self._map.items():
            print(f"Middleware Registered -- {key}, {value}")

    def get(self, key):
        if key in self._map:
            return self._map[key]
        else:
            print('Middleware not found')

    def register(self, key, value):
        self._map[key] = value

    def has(self, key):
        return key in self._map

    def delete(self, key):
        if key in self._map:
            del self._map[key]
            return True
        return False


class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
            cls._instance.middleware_register = MiddlewareRegister()
        return cls._instance

    @property
    def instance(self):
        return self.middleware_register


# To get the singleton instance of MiddlewareRegister
middleware_register = Singleton().instance
