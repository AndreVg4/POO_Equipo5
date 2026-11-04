
# Clase base para representar un nodo de una red IoT.
# Contiene los atributos y métodos comunes para todos los dispositivos.

class NodoIoT:

    def __init__(self, id_dispositivo: str, ip: str, ubicacion: str):
        self.id_dispositivo = id_dispositivo
        self.ip = ip
        self.ubicacion = ubicacion
        self.conectado = False

    def conectar(self):         #Establece el estado del nodo como conectado.
        self.conectado = True
        print(f"[{self.id_dispositivo}] Nodo conectado correctamente.")

    def enviar_telemetria(self): # Método para representar el envío de telemetría.

        if self.conectado:
            print(
                f"[{self.id_dispositivo}] Enviando telemetría "
                f"desde {self.ubicacion}..."
            )
        else:
            print(
                f"[{self.id_dispositivo}] No se puede enviar telemetría: "
                "el nodo está desconectado."
            )
