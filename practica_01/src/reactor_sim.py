import os
import random

# Lista global para simular un registrador de eventos (Event Logger) tipo SCADA/HMI
# Esto evita que los mensajes de acción se borren al limpiar la pantalla
historial_eventos = []

def registrar_evento(mensaje: str):
    """Agrega un evento al historial y mantiene solo los últimos 5 para que no desplace la pantalla."""
    historial_eventos.append(mensaje)
    if len(historial_eventos) > 5:
        historial_eventos.pop(0)

def limpiar_pantalla():
    """Limpia la terminal según el sistema operativo (cls para Windows, clear para Unix)."""
    os.system('cls' if os.name == 'nt' else 'clear')

# ==============================================================================
#                                  CLASES 
# ==============================================================================
class Actuador:
    def __init__(self, nombre: str):
        # Atributos de estado del actuador
        self.nombre = nombre
        self.rango_operacion_min = 0.0   # Límite mínimo de operación (0%)
        self.rango_operacion_max = 100.0 # Límite máximo de operación (100%)
        self.estado = False              # Estado lógico de encendido: False = OFF, True = ON
        self.punto_operacion = 0.0       # Porcentaje actual de operación
   def encender(self):
       #cambie el estado a ON y registra el envnto
       self.estado = True #ON
       registrar_evento(f" {self.nombre} ENCENDIDO")

   def apagar(self):
       #Cambia el estado  a OFF y registra el evento
       self.estado = False # OFF
       registrar_eveto(f"{self.nombre }APAGADO")

  def ajustar(self, valor : float): 
      if self.rango_operacio_min <= valor <= self.rango_operacion_max:
          self.punto_operacion = valor
          registrar_evento(f"{self.nombre} Punto de operacion ajustado al {self.punto_operacion}")
          else:
            registrar_evento(f"[⚠️ ERROR] {self.nombre} -> Valor {valor}% fuera de rango (0% - 100%).")

    def info(self) -> str:
        #Retorna una cadena con el estado formateado del actuador
        estado_str = "ON" if self.estado else "OFF"
        return f"{self.nombre:<20} | Estado: {estado_str:<3} | Punto Op: {self.punto_operacion:>5.1f}% | Rango: [0.0% - 100.0%]"


class Sensor:
    def __init__(self, nombre: str, variable_fisica: str, rango_min: float, rango_max: float, sensibilidad: float, decimales_medicion: int, unidad: str):
        # Atributos de especificación técnica del sensor
        self.nombre = nombre
        self.variable_fisica = variable_fisica
        self.rango_min = rango_min
        self.rango_max = rango_max
        self.sensibilidad = sensibilidad
        self.decimales_medicion = decimales_medicion
        self.unidad = unidad
       


