# REQUISITOS
* Sistema de mensajería instantánea anónima
	* **Validación**: poder enviar un mensaje a otro usuario.
* Posibilidad de crear chat grupales
	* **Validación**: crear un grupo con varios usuarios
* Posibilidad de crear y suscribirse a canales (como Telegram)
	* **Validación**: crear un canal y subscribir a un usuario al mismo.
* No identificación al registrarse (tfno, email, dni…)
	* **Validación**: poder crear una cuenta sin especificar datos personales.
* Opción para compartir documentos (imagen, videos, audios…)
	* **Validación**: Que un usuario pueda enviar documentos y el usuario que los recibe pueda abrirlos y visualizarlos.
* Funcionalidad para censurar caras de personas en una foto
	* **Validación**: Que al descargar una imagen, las caras salgan censuradas.
* Emplear tecnología blockchain.
	* **Validación**: Mostrar en qué blockchain está desplegada la aplicación.
* Poder hacer llamadas, videollamadas…
	* **Validación**: Que un usuario pueda llamar a otro usuario y viceversa.
* Garantizar entrega de mensajes efectiva y rápida
	* **Validación**: enviar un mensaje y comprobar que llega al usuario correcto dentro del tiempo estipulado.
* Aplicación web, móvil (ios, android), escritorio
	* **Validación**: poder descargar una aplicación al móvil o al ordenador. Poder acceder desde la web.
* Accesible desde cualquier ubicación
	* **Validación**: intentar conectarse a la red desde diferentes ubicaciones físicas.
* Protocolo de red P2P distribuida, para garantizar la descentralización. No servidores.
	* **Validación**: demostrar que los usuarios son nodos en una red descentralizada, sin que haya servidores que almacenen información
* Garantizar almacenamiento local y cifrado de los mensajes (en el dispositivo del usuario)
	* **Validación**: verificar que los archivos que contienen los mensajes no están en texto claro.
* Tiempo de vida de los mensajes
	* **Validación**: enviar un mensaje con un tiempo de vida determinado y verificar que se elimina al transcurrir el plazo estipulado.
* Posibilidad de intercambio de dinero (criptomonedas…). 
	* **Validación**: Tener una billetera de criptomonedas y poder realizar transacciones de criptomonedas con otros usuarios.
* Compatibilidad con billeteras crypto (de forma anónima).
	* **Validación**: Conectar con éxito una billetera a la aplicación
* Garantía de cumplimiento de un contrato antes de que se efectúe el pago (intermediario)
	* **Validación**: Intentar cobrar un pago sin haber cumplido las condiciones y comprobar que la aplicación no lo permite
* Posibilidad de configurar idiomas
	* **Validación**: Configurar la aplicación en varios idiomas, como español, inglés, etc…
* Interfaz intuitiva
	* **Validación**: el cliente puede usar la aplicación sin que se le explique como hacerlo.
* Identificación dentro de la aplicación a través de códigos generados aleatoriamente al darse de alta.
	* **Validación**: mostrar al cliente los códigos generados.
* Posibilidad de compartir “nombre de usuario” o “hash” (a través de códigos QR).
	* **Validación**: se genera un código QR y se establece comunicación cuando el otro usuario lo escanea.
* No te puedes comunicar con alguien si no conoces su hash (garantizar fiabilidad).
	* **Validación**: Demostrar que no hay otra manera de poder enviar un mensaje a alguien.
* Posibilidad de compartir usuarios (mediante validación del usuario que se comparte).
	* **Validación**: compartir un usuario con un tercero y verificar que no se comparte hasta que el usuario compartido acepte.
* No se puede hacer capturas de pantalla
	* **Validación**: intentar hacer una captura de pantalla y verificar que la aplicación no lo permite.
* Cifrado de los mensajes enviados.
	* **Validación**: capturar el tráfico intercambiado y comprobar que está cifrado. 
* No comunicar nunca dos nodos directamente sino emplear al menos un nodo intermediario (onion routing).
	* **Validación**: Se realiza una traza de un mensaje y se comprueba que hace al menos dos saltos entre los nodos de la red.
* Si no está conectado un usuario no se puede enviar mensaje, pero se puede intentar seguir enviando hasta que se conecte.
	* **Validación**: enviar un mensaje a un usuario no conectado. Verificar que no se envía. Conectar el usuario y verificar que le llega el mensaje.
* Implementar sistema de notificaciones
	* **Validación**: Le llega una notificación al usuario cuando recibe un mensaje.
* Garantizar que no se pierde la conexión si te cambias de red (movilidad)
	* **Validación**: Cambiar de red y ver que sigues conectado a la aplicación.
* Evitar que los usuarios puedan conectarse desde una red pública
	* **Validación**: Intentar conectarse desde una red pública y comprobar que la aplicación no lo permite
* Poder programar envíos (de mensajes, dinero, etc.).
	* **Validación**: Se programa un envío y se realiza cuando debe.
