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

