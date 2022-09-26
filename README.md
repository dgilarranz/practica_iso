* Sistema de mensajería instantánea anónima
    * **Validación**: poder enviar un mensaje a otro usuario.
    * Como una app típica de mensajería, tiene las mismas funcionalidades, con la diferencia de que no se conocen datos personales del usuario. Cuando se contacte uno o varios usuarios la única referencia del usuario es su nickname. 
    * Se mandaran los mensajes al servidor y el servidor los redirigirá al usuario destino.
* Posibilidad de crear chat grupales
    * **Validación**: crear un grupo con varios usuarios
    * Al igual que se pueden mandar mensajes a usuarios concretos, también se pueden crear grupos al que estén adscritos distintos usuarios y todos los mensajes lleguen a esos usuarios.
    * Los mensajes se mandaran al servidor y el servidor es el encargado de hacer llegar todos los mensajes mandados a los usuarios del grupo. El servidor también se encarga de guardar el historial de mensajes del grupo.
* Posibilidad de crear y suscribirse a canales (como Telegram)
    * **Validación**: crear un canal y subscribir a un usuario al mismo.
    * Un canal no es un grupo, la diferencia es que hay como un usuario o varios que tienen el rol de administrador, ellos son los únicos que pueden mandar mensaje al canal, los usuarios suscritos al canal únicamente leen el canal. 
    * Los usuarios tienen la opción de compartir el canal mediante un código QR o un enlace. Para entrar en los canales puede ser directamente a través del enlace pero el administrador puede establecer que antes de entrar haya que solicitar el acceso y ellos se encargaran de dar acceso a los usuarios que consideren.
* No identificación al registrarse (tfno, email, dni…)
    * **Validación**: poder crear una cuenta sin especificar datos personales.
    * En el momento de registrarse no se van a solicitar datos personales, unicamente se solicitará al usuario que establezca un nickname, el cual será único, si ya esta ocupado por otro usuario no se permitirá completar el registro. Para garantizar el anonimato es suficiente con nombre de usuario y password.
* Opción para compartir documentos (imagen, videos, audios…)
    * **Validación**: Que un usuario pueda enviar documentos y el usuario que los recibe pueda abrirlos y visualizarlos
    * Durante la conversación entre distintos usuarios existe la posibilidad de adjuntar archivos de distinto tipo ya sea jpg, mp4,mp3,pdf,etc. El usuario receptor deberá tener un programa/aplicación capaz de leer los archivos que se envien ya que esta aplicación no va a tener la opción de abrirlos, a excepción de las fotos, videos y audios que la app si que será capaz de leerlo.
* Funcionalidad para editar fotos (censurar caras, opción de que se vea solo 1 vez, recortar,etc)
    * **Validación**: Que al descargar una imagen, las caras salgan censuradas.
    * A la hora de enviar fotos la aplicación va a integrar un editor de fotos el cual va orientado a la privacidad, el cual tiene la opción de establecer que las fotos solo se pueden abrir una vez, de censurar las caras, de pixelar, poner password a la foto,etc).
    * Entonces cuando se envían las fotos se pueden enviar directamente, o pasar por el editor de fotos antes de enviarlo, una vez censurada una cara y da al ok, no es reversible, es decir, no es posible “limpiar” o “esclarecer” la cara de la foto.
* Emplear tecnología blockchain.
    * **Validación**: Mostrar en qué blockchain está desplegada la aplicación.		La funcionalidad de la aplicación es garantizar la seguridad de los mensajes de los usuarios de la aplicación. Para ello implementaremos una cadena de bloques que nos permita realizar una transferencia de información que no requiera de un  intermediario central. La información está distribuida en múltiples nodos, independientes entre sí. Garantizamos que sea prácticamente imposible que terceras personas puedan acceder a la información de los usuarios (mensajes, fotos…)
* Poder hacer llamadas, videollamadas…
    * **Validación**: Que un usuario pueda llamar a otro usuario y viceversa.
    * Se busca implementar una funcionalidad en la aplicación que permita a los usuarios disponer de distintas formas de comunicarse además de los mensajes y las fotos. Estas serían llamadas o videollamadas, que permiten la comunicación en directo mediante audio y video entre los usuarios. Requiere que se garantice la privacidad de estas conversaciones para que nadie ajeno a la conversación pueda acceder.
* Garantizar entrega de mensajes efectiva y rápida
    * **Validación**: enviar un mensaje y comprobar que llega al usuario correcto dentro del tiempo estipulado.
    *Un requisito principal de una empresa de mensajería es que los mensajes se envíen cumpliendo unos requisitos. Entre ellos, podemos mencionar una entrega efectiva de mensajes (de forma correcta, íntegra y al usuario seleccionado, sin perderse por el camino). Además, esta entrega debe realizarse en el mínimo tiempo posible. 
* Aplicación web, móvil (ios, android), escritorio
    * **Validación**: poder descargar una aplicación al móvil o al ordenador. Poder acceder desde la web.
    * Tratamos de garantizar el acceso de los usuarios a nuestra aplicación desde las máximas plataformas posibles. Para ello, crearemos una aplicación de escritorio para los usuarios de ordenador, una aplicación móvil que esté disponible en los dos sistemas operativos principales (android y ios), además de tener una aplicación web. En cualquier caso, siempre que la comunidad demande una nueva forma de acceder a la aplicación, se estudiaría siempre que no comprometa la viabilidad de la aplicación, así como sus principios básicos. 
* Accesible desde cualquier ubicación
    * **Validación**: intentar conectarse a la red desde diferentes ubicaciones físicas.
    * Queremos que nuestra aplicación sea accesible para todos los usuarios del mundo, y que ellos puedan comunicarse entre sí. Es decir, queremos evitar cualquier tipo de restricción geográfica dentro de nuestra aplicación. 
    * Para ello, debemos generar una app que sea genérica para todos los usuarios alrededor del mundo, pero la app en ningún momento debe saber tu ubicación, puesto que violaría uno de los requisitos principales de privacidad. 
* Protocolo de red P2P distribuida, para garantizar la descentralización. No servidores.
    * **Validación**: demostrar que los usuarios son nodos en una red descentralizada, sin que haya servidores que almacenen información
    * La comunicación se realizará mediante el protocolo P2P, el cual está compuesto por una serie de nodos con un comportamiento entre sí. Nos permiten el intercambio directo de información entre los ordenadores que estén interconectados. La principal ventaja es que nos permite la descentralización, debido a la ausencia de servidores que puedan almacenar la información.
* Garantizar almacenamiento local y cifrado de los mensajes (en el dispositivo del usuario).
    * **Validación**: verificar que los archivos que contienen los mensajes no están en texto claro.
    * Los mensajes de los usuarios no deben almacenarse fuera de sus dispositivos de manera centralizada, para evitar que una brecha de seguridad exponga las conversaciones mantenidas.
* Tiempo de vida de los mensajes
    * **Validación**: enviar un mensaje con un tiempo de vida determinado y verificar que se elimina al transcurrir el plazo estipulado.
    * El usuario debe tener la posibilidad de establecer un tiempo de vida máximo para sus mensajes, de manera que una vez venza el plazo determinado, los mensajes se borren de manera permanente tanto de sus dispositivo como del dispositivo del destinatario.
* Posibilidad de intercambio de dinero (criptomonedas…). 
    * **Validación**: Tener una billetera de criptomonedas y poder realizar transacciones de criptomonedas con otros usuarios.
    * La aplicación debe proporcionar a sus usuarios la posibilidad de realizar intercambios monetarios con los usuarios con los que mantengan conversaciones, de manera que se puedan llevar a cabo negocios anónimos a través de la aplicación.
* Compatibilidad con billeteras crypto (de forma anónima).
    * **Validación**: Conectar con éxito una billetera a la aplicación
    * Es imperativo que la aplicación permita el intercambio de criptomonedas, por lo que debe tener una interfaz que permita a los usuarios asociar sus billeteras cripto y poder emplearlas en los intercambios definidos anteriormente.
* Garantía de cumplimiento de un contrato antes de que se efectúe el pago (intermediario)
    * **Validación**: Intentar cobrar un pago sin haber cumplido las condiciones y comprobar que la aplicación no lo permite
    * La aplicación debe proporcionar algún sistema de arbitraje que permita a compradores y vendedores establecer un “contrato” verificable (automáticamente o a través de un tercero). El comprador depositará el dinero en una cuenta ajena a los participantes (bien a la aplicación o al tercero de confianza) y no podrá ser retirado por el vendedor hasta que la aplicación (o el tercero) dé por cumplidos los términos del contrato.
* Posibilidad de configurar idiomas
    * **Validación**: Configurar la aplicación en varios idiomas, como español, inglés, etc…
    * La aplicación debe permitir a los usuarios configurar su idioma de preferencia y mostrar todos los elementos de la interfaz en el mismo, para facilitar su uso por individuos de diferentes países.
* Interfaz intuitiva
    * **Validación**: el cliente puede usar la aplicación sin que se le explique como hacerlo.
    * La interfaz de usuario debe ser lo más simple y autoexplicativa posible, de manera que sea utilizable sin problemas por un usuario nuevo a la aplicación con una mínima curva de aprendizaje. Un usuario nuevo debe saber emplear la aplicación basándose en experiencias previas con aplicaciones similares.
* Identificación dentro de la aplicación a través de códigos generados aleatoriamente al darse de alta.
    * **Validación**: mostrar al cliente los códigos generados.
    * Una función criptográfica hash- usualmente conocida como “hash”- es un algoritmo matemático que transforma cualquier bloque arbitrario de datos en una nueva serie de caracteres con una longitud fija. Independientemente de la longitud de los datos de entrada, el valor hash de salida tendrá siempre la misma longitud.
    * Un código QR es la evolución del código de barras. Es un módulo para almacenar información en una matriz de puntos o en un código de barras bidimensional. La matriz se lee en el dispositivo móvil por un lector específico (lector de QR).
* Posibilidad de compartir “nombre de usuario” o “hash” (a través de códigos QR).
    * **Validación**: se genera un código QR o un código hash y se establece comunicación cuando el otro usuario lo escanea.
* Una vez generado el código, no te puedes comunicar con alguien si no conoces su hash (garantizar fiabilidad).
    * **Validación**: Demostrar que no hay otra manera de poder enviar un mensaje a alguien.
    * La clave de la comunicación en nuestro protocolo es identificar a los usuarios mediante “hashes” como se hace en la tecnología blockchain. Esto permite un pseudo-anonimato automáticamente que garantiza una capa extra de despersonalización. Un usuario es identificado únicamente mediante dicho hash el cual no tiene una vinculación directa a su persona salvo que el mismo quiera revelar que le pertenece.
* Posibilidad de compartir usuarios (mediante validación del usuario que se comparte).
    * **Validación**: compartir un usuario con un tercero y verificar que no se comparte hasta que el usuario compartido acepte.
    * Para garantizar la no divulgación de información personal, es el propio usuario “dueño del hash” el que debe aceptar si su perfil puede ser compartido por un usuario a un tercero. Esto permite evitar que la información de un usuario sea transmitida sin su consentimiento. El hash tendría que ser cambiante o estar a su vez encriptado para solucionar el problema de que lo apuntase en un papel y lo compartiera “manualmente” 
* No se puede hacer capturas de pantalla
    * **Validación**: intentar hacer una captura de pantalla y verificar que la aplicación no lo permite.
    * Dentro de nuestra aplicación Front-End debemos evitar la posibilidad de que los usuarios puedan almacenar pantallazos de la misma. Esto añade una capa de seguridad extra que desincentiva a múltiples usuarios a extraer información de la aplicación para compartirla externamente. Debería bloquearse esta funcionalidad en todas las plataformas donde se pueda utilizar la app web. Podría implementarse con un mensaje de “Están prohibidas las capturas de pantalla” o que al realizarse, determinadas secciones de información delicada quedasen borrosas e ilegibles en el archivo de imagen.
 
* Cifrado de los mensajes enviados.
    * **Validación**: capturar el tráfico intercambiado y comprobar que está cifrado. 
    * Es crucial que si alguien quisiera utilizar algún capturador de paquetes estilo Wireshark o similares se encontrase con una serie de paquetes altamente cifrados para evitar o complicar lo máximo posible la identificación del contenido  de los mismos. Esto añade una capa de seguridad extra en los ataques a la  plataforma a través de la red.

* No comunicar nunca dos nodos directamente sino emplear al menos un nodo intermediario (onion routing).
    * **Validación**: Se realiza una traza de un mensaje y se comprueba que hace al menos dos saltos entre los nodos de la red.
    * Una de las bases de nuestra aplicación consiste en la integración de las bases del protocolo de Onion utilizado en redes o apps como Tor Browser. La eficacia reside en que todo contenido divulgado a través de la app nunca podría ir directamente al destino al que se dirige. Como mínimo el usuario (sin el realizarlo) estaría utilizando un nodo externo como intermediario (similar a un proxy) que añadiría una capa extra de anonimidad. Además sería altamente recomendable utilizar múltiples nodos para aumentar la seguridad.
* Si no está conectado un usuario no se puede enviar mensaje, pero se puede intentar seguir enviando hasta que se conecte.
    * **Validación**: enviar un mensaje a un usuario no conectado. Verificar que no se envía. Conectar el usuario y verificar que le llega el mensaje.
    * Un usuario no debería poder recibir mensajes si no está conectado a laplicación. Pese a que los mensajes puedan ser enviados desde el emisor, quedarían almacenados en una especie de buffer intermedio el cual enviaría finalmente todo el contenido de golpe al receptor cuando éste decidiese conectarse para recibirlo.
* Implementar sistema de notificaciones
    * **Validación**: Le llega una notificación al usuario cuando recibe un mensaje.
    * Una notificación es un mensaje que muestra Android fuera de la IU de la app para proporcionar al usuario recordatorios, mensajes de otras personas y otra información puntual de la app. Los usuarios pueden presionar la notificación para abrir la app o realizar una acción directamente desde la notificación.
    * Las notificaciones tienen que llegar incluso cuando el usuario no use el móvil.
    * Hay opción de que el usuario pueda desactivar las notificaciones para que no le lleguen.
* Garantizar que no se pierde la conexión si te cambias de red (movilidad)
    * **Validación**: Cambiar de red y ver que sigues conectado a la aplicación.    * Si cambiamos de red manual o automáticamente, o cambiamos de red a datos móviles, deberemos de seguir conectados a internet con la app.
* Esta función no está habilitada de manera predeterminada; el dispositivo le indica al usuario que habilite la función la primera vez que experimenta una conectividad Wi-Fi deficiente.
* Evitar que los usuarios puedan conectarse desde una red pública
    * **Validación**: Intentar conectarse desde una red pública y comprobar que la aplicación no lo permite.
    * Las wifis públicas son aquellas que no están protegidas por una contraseña y nos permiten conectarnos a Internet de una forma cómoda y rápida. Estas redes no cifran la información que se transmite a través de ellas, por lo que no son seguras. También son aquellas que aun teniendo contraseña se acceso, se conectan muchas usuarios a ellas. Comúnmente las identificamos como wifis gratuitas.
* Poder programar envíos (de mensajes, dinero, etc.).
    * **Validación**: Se programa un envío y se realiza cuando debe.
    * Para programar un mensaje o envío de dinero se puede hacer desde el acceso directo o abriendo directamente la aplicación. Se selecciona destinatario, se programa el día y la hora, se añade contenido si se desea (foto, vídeo, archivo, etc…) y se presiona el botón de aceptar en la parte inferior derecha.
