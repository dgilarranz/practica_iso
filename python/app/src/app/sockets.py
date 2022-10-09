import asyncio
from asyncore import write
from dis import findlinestarts
from sys import stderr
from xmlrpc.client import Boolean

class ConnectionManager():
    def __init__(self, port=54321, separator='\N{END OF MEDIUM}', end_message_indicator='\N{END OF TRANSMISSION}') -> None:
        # Lanzamos el servicio de escucha en el puerto PORT
        self.port = port
        self.last_port = port
        self.timeout = 5

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

        if contact_hash not in self.messages:
            # Si el usuario no está registrado, se registra la conexión
            self.messages[contact_hash] = []

            # Devolvemos un código indicando que se ha registrado la conexión
            response = f'{self.user_registered_code}{self.end_message}'
            writer.write(response.encode('utf-8'))
            await writer.drain()
        else:
            # Si el usuario está registrado, se añade el mensaje al diccionario
            self.messages[contact_hash].append(message)
            
            # Devolvemos un código indicando que se ha enviado el mensaje
            response = f'{self.message_delivered_code}{self.end_message}'
            writer.write(response.encode('utf-8'))
            await writer.drain()
        
        writer.close()

    async def send_message(self, ip: str, port: int, contact_hash: str, message: str) -> Boolean:
        # Establecemos una conexión con el destino
        reader, writer = await asyncio.open_connection(ip, port)

        # Enviamos el mensaje
        data = f'{contact_hash}{self.hash_message_separator}{message}{self.end_message}'
        writer.write(data.encode('utf-8'))
        await writer.drain()

        # Esperamos a recibir el código de confirmación
        response = ''
        try:
            response = await asyncio.wait_for(
                reader.readuntil(self.end_message.encode('utf-8')), 
                timeout=self.timeout
            )
        except asyncio.TimeoutError:
            print("Error: Timeout expirado esperando la respuesta", stderr)
        finally:
            writer.close()
            await writer.wait_closed()
        
        return response.decode('utf-8').strip(self.end_message) == self.message_delivered_code