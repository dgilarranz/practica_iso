import asyncio
from asyncore import write
from dis import findlinestarts
from sqlite3 import connect
from sys import stderr
from xmlrpc.client import Boolean
from app.observer import Subject

class ConnectionManager(Subject):
    def __init__(self, port=54321, separator='\N{END OF MEDIUM}', end_message_indicator='\N{END OF TRANSMISSION}') -> None:
        # Lanzamos el servicio de escucha en el puerto PORT
        self.port = port
        self.last_port = port
        self.timeout = 5
        self.retry_time = 5

        # Separadores y códigos para los mensajes
        # formato petición: HASH_USUARIO{hash_message_separator}MENSAJE{end_message}
        # formato respuesta: CÓDIGO{end_message}
        self.hash_message_separator = separator
        self.end_message = end_message_indicator
        self.user_registered_code = '200'
        self.message_delivered_code = '201'

        # Inicialmente, no mensajes de ningún usuario
        self.messages: dict[str, list[str]] = {}
    
    async def start_service(self) -> None:
        server = await asyncio.start_server(self.answer_requests, host='', port=self.port)

        async with server:
            await server.serve_forever()

    async def answer_requests(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        # Al recibir una conexión, comprobamos si el hash se corresponde a una sesión ya establecida
        data = await reader.readuntil(self.end_message.encode('utf-8'))
        data = data.decode('utf-8').split(sep=self.hash_message_separator)
        
        contact_hash = data[0]
        message = data[1].strip(self.end_message)

        # Se comprueba si es la primera vez que se recibe un mensaje de este emisor
        if contact_hash not in self.messages:
            # Si el usuario no está registrado, se registra la conexión
            self.messages[contact_hash] = []

            # Devolvemos un código indicando que se ha registrado la conexión
            response = f'{self.user_registered_code}{self.end_message}'
            writer.write(response.encode('utf-8'))
            await writer.drain()
        
        # Si se ha adjuntado un mensaje, se añade
        if len(message) > 0:
            # Si el usuario está registrado, se añade el mensaje al diccionario
            self.messages[contact_hash].append(message)
            
            # Devolvemos un código indicando que se ha enviado el mensaje
            response = f'{self.message_delivered_code}{self.end_message}'
            writer.write(response.encode('utf-8'))
            await writer.drain()
        
        writer.close()

    async def send_message(self, ip: str, port: int, contact_hash: str, message: str) -> Boolean:
        print(message)
        # Abrimos la conexión, si hay errores se intenta hasta lograrse
        connected = False
        while not connected:
            try:
                # Establecemos una conexión con el destino
                reader, writer = await asyncio.open_connection(ip, port)
                connected = True
            except Exception:
                print("Error abriendo la conexión")
                await asyncio.sleep(self.retry_time)

        # Enviamos el mensaje
        data = f'{contact_hash}{self.hash_message_separator}{message}{self.end_message}'
        writer.write(data.encode('utf-8'))
        await writer.drain()

        # Esperamos a recibir el código de confirmación, intentando enviar el mensaje hasta conseguirlo
        response = ''
        sent = False
        while not sent:
            try:
                response = await asyncio.wait_for(
                    reader.readuntil(self.end_message.encode('utf-8')), 
                    timeout=self.timeout
                )
                sent = True
            except asyncio.TimeoutError:
                print("Error: Timeout expirado esperando la respuesta", stderr)
                await asyncio.sleep(self.retry_time)

        writer.close()
        await writer.wait_closed()
        
        return response.decode('utf-8').strip(self.end_message) == self.message_delivered_code
    
    def get_messages(self, hash: str) -> list[str]:
        # Obtenemos los mensajes (si no hay mensajes -> lista vacía)
        messages = []
        if hash in self.messages.keys():
            # Si había mensajes asociados al hash, vaciamos la cola de mensajes
            messages = self.messages[hash].copy()
            self.messages[hash] = []
        
        # Devolvemos los mensajes obtenidos
        return messages