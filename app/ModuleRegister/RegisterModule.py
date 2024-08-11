class Module:
    def __init__(self):
        self._map = {}

    def register(self, key, value):
        self._map[key] = value

    def list(self):
        for key in self._map:
            print(f"module installed -- {key}")

    def has(self, key):
        return key in self._map

    def delete(self, key):
        return self._map.pop(key, None) is not None


class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
            cls._instance.module = Module()
        return cls._instance

    @property
    def instance(self):
        return self.module


# To get the singleton instance of Module
register_module = Singleton().instance
