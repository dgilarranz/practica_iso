from multiprocessing.connection import wait
from unittest.mock import patch
from app.sockets import ConnectionManager
from app.observer import Subject
import asyncio
import pytest    

@pytest.mark.asyncio
async def test_crear_puerto_escucha() -> None:
    # Verificamos que es posible establecer una conexión con el puerto 54321
    port = 54321
    cm = ConnectionManager(port)
    server_task = asyncio.create_task(cm.start_service())
    
    # Esperamos a que arranque el servidor
    await asyncio.sleep(1)

    reader, writer = await asyncio.open_connection('127.0.0.1', port)
    
    # Enviamos un hash de prueba, simulando ser un usuario
    data = f'hash_prueba{cm.hash_message_separator}{cm.end_message}'
    writer.write(data.encode('utf-8'))
    await writer.drain()

    # Verificamos que recibimos como respuesta el código user_registered
    response = await reader.readuntil(cm.end_message.encode('utf-8'))
    assert response.decode('utf-8').strip(cm.end_message) == cm.user_registered_code

    # Detenemos el servidor
    server_task.cancel()

    # Esperamos a que se libere detenga el servidor
    await asyncio.sleep(10)


# Nota: parcheamos el diccionario para que parezca que el usuario hash_prueba está registrado
# y así poder enviarle un mensaje 
@pytest.mark.asyncio
async def test_enviar_mensaje() -> None:
    # Lanzamos el servicio de esucha
    port = 54321
    cm = ConnectionManager(port)
    server_task = asyncio.create_task(cm.start_service())
    
    # Enviamos un mensaje a hash_prueba
    user = 'hash_prueba'
    message = 'mensaje'
    
    with patch.dict(cm.messages, {user: []}):
        response = await cm.send_message('127.0.0.1', port, user, message)

        # Verificamos que se ha añadido el mensaje a la cola
        assert cm.messages[user][0] == message
        assert response == True

    # Detenemos el servidor
    server_task.cancel()

    # Esperamos a que se libere el puerto
    await asyncio.sleep(10)

def test_get_messages():
    # Mockeamos el diccionario de mensajes
    cm = ConnectionManager()
    with patch.object(cm, 'messages', {'hash_prueba': ['mensaje']}):
        assert cm.get_messages('hash_prueba')[0] == 'mensaje'

def test_connection_manager_is_instance_of_subject():
    cm = ConnectionManager()
    assert isinstance(cm, Subject)

def test_connection_manager_initialises_super_class():
    cm = ConnectionManager()
    assert cm.subscribers is not None


@pytest.mark.asyncio
async def test_connection_manager_notifies_subscribers_on_message_received_for_existing_chat():
    cm = ConnectionManager(54322)
    server_task = asyncio.create_task(cm.start_service())
    await asyncio.sleep(1)

    with patch.object(cm, "notify") as mock_notify:
        cm.messages["chat_prueba"] = ["mensaje de prueba"]
        message_task = asyncio.create_task(cm.send_message("127.0.0.1", 54322, "chat_prueba", "otro mensaje"))
        await asyncio.sleep(1)
        mock_notify.assert_called_once()
    
    server_task.cancel()
    message_task.cancel()

@pytest.mark.asyncio
async def test_connection_manager_does_not_notify_if_message_empty():
    cm = ConnectionManager(54322)
    server_task = asyncio.create_task(cm.start_service())
    await asyncio.sleep(1)

    with patch.object(cm, "notify") as mock_notify:
        cm.messages["chat_prueba"] = ["mensaje de prueba"]
        message_task = asyncio.create_task(cm.send_message("127.0.0.1", 54322, "chat_prueba", ""))
        await asyncio.sleep(1)
        mock_notify.assert_not_called()
    
    server_task.cancel()
    message_task.cancel()
