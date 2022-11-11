from app.usuario import Usuario
from app.sockets import ConnectionManager

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        # Si no existe ya una instancia de la clase, se crea
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class ConfigManager(metaclass=Singleton):  
    user = None
    connection_manager = None