#Clase base para representar un nodo de una red IOT.
#en esta estan los atributos y metodos comunes para todos los dispositivos.
class NodoIOT:
  def __init__(self, id_dispositivo: str, ip: str, ubicacion: str): 
    self.id_dispositivo = id:dispositivo
    self.ip= ip
    self.ubicacion = ubicacion
    self.conesctado = False

def conctar(self):  #Establece e estado del nodo como conectado.
  self.conectado = True
  print(f"[{self.id_dispositivo}] Nodo conectado correctamente.")

def enviar_telemetria(self): # metodo para representar el envio de telemetria.
  if self.conectado:
    print(
        f"[{self.id_dispositivo}] Enviando telemetria"
        f"desde {self.ubicacion} ... "  
    )
  else:
    print(
      f"[{self.id_dispositivo}] Nose puede enviar Telemetria "
      "el nodo esta desconectado"
    )
