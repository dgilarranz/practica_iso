Carpeta para los Smart Contracts desarrollados.

Consideraciones del script.
*Pese a que es posible el uso de envs para los datos privados como las direcciones de las carteras de los usuarios o sus PRIVATE_KEYS hemos preferido utilizar scanners para evitar que ningún dato quede almacenado (ya sea voluntariamente o por error) en cualquier fichero

El script necesita varios datos de input para funcionar
1: La dirección/cartera FROM (desde donde se enviarán los tokens)

2: La CLAVE PRIVADA de dicha dirección/cartera (para poder realizar las transacciones desde un script externo como este)

3: La dirección del **contrato** del Token que queremos enviar.

Toda criptomoneda tiene un contrato (SW) asociado mediante el cual se identifica la posesión de dicho activo y se permite interactuar con las funciones que lo describen.

Este programa admite cualquier activo existente en la blockchain de prueba de Goerli. 

En caso de querer adaptarlo para otras blockchains es necesario sustituir la variable "infura_url" por un RPC (punto de entrada) valido para dicha blockchain.


4: La cantidad a enviar (en valores unitarios). El programa hace por sí solo la conversión de ETH a Wei. 

(ETH - WEI) es el equivalente a (EUR - CENT) donde 1 eth son 10^18 weis.


Si se quiere comprobar si la transacción se ha realizado correctamente utilizar la herramienta "Goerli Etherscan" indexando con la dirección origen/destino utilizada para la transacción. 


