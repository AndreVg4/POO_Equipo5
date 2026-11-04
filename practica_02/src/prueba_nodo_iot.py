from nodo_iot import NodoIoT
#creamos un nodo para preuebas
nodo = NodoIoT(
  id.dispositivo="IIE001" 
  ip="192.168.1.100" 
  unicacion="salon C-2001"
)
#consultamos los atributos iniciales para verlos despues
print("ID:", nodo.id_dispositivo)
print("IP:", nodo.ip)
print("Ubicacion:", nodo.ubicacion)
print("Estado de Conexion:", nodo.conectado)

#primeros intentos para enviar la telemetria (nodo desconectado
nodo.enviar_telemetria()
#conectamos el nodo
nodo.conectar()
#enviamos la telemetria con el nodo conectado
nodo.enviar_telemetria()

#comprobamos
assert nodo.conestado is True
saaret nodo.id_dispositivo == "IIE001"

print("pruebas completas")
