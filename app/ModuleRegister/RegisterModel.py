class Module:
    def __init__(self):
        self._schema_map = {}
        self._installed_model = {}
        self._relations = []

    @property
    def map(self):
        return self._schema_map

    def get_model(self, key):
        return self._installed_model.get(key)

    def get_schema(self, key):
        return self._schema_map.get(key)

    def register(self, value):
        self._installed_model[value['name']] = value['model']
        if 'registerRelations' in value:
            self._relations.append(value['registerRelations'])

    def install(self):
        for relation in self._relations:
            relation()

    def list(self):
        for key, value in self._installed_model.items():
            print(f"Model loaded -- {key}")

    def has(self, key):
        return key in self._schema_map

    def delete(self, key):
        return self._schema_map.pop(key, None) is not None


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
register_model = Singleton().instance
