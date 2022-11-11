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

    def get_connection_manager(self) -> ConnectionManager:
        return self.connection_manager

    def set_connection_manager(self, cm: ConnectionManager):
        self.connection_manager = cm

    def get_user(self) -> Usuario:
        return self.user

    def set_user(self, user: Usuario):
        self.user = user