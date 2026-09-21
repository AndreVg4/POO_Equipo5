
       


#!/usr/bin/env python3
"""
EE: Programación Orientada a Objetos (UV)
Versión 1.0.0: Simulador de Reactor Químico en Python
Lazo cerrado térmico/barométrico con HMI estático e Interlocks de seguridad.
"""

import os
import random

# ==============================================================================
# GESTOR DE EVENTOS Y TERMINAL
# ==============================================================================
historial_eventos = []

def registrar_evento(mensaje: str):
    historial_eventos.append(mensaje)
    if len(historial_eventos) > 6:
        historial_eventos.pop(0)

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


# ==============================================================================
# HARDWARE SIMULADO: ACTUADORES Y SENSORES
# ==============================================================================
class Actuador:
    def __init__(self, nombre: str, tipo_control: str = "PROPORCIONAL"):
        self.nombre = nombre
        self.tipo_control = tipo_control  # "PROPORCIONAL" o "DIGITAL"
        self.rango_operacion_min = 0.0
        self.rango_operacion_max = 100.0
        self.estado = False               # False = OFF/Cerrada, True = ON/Abierta
        self.punto_operacion = 0.0        # Porcentaje actual (0.0% a 100.0%)

    def encender(self):
        self.estado = True
        self.punto_operacion = 100.0
        registrar_evento(f"[+] {self.nombre} -> Estado: ENCENDIDO (ON/100%)")

    def apagar(self):
        self.estado = False
        self.punto_operacion = 0.0
        registrar_evento(f"[-] {self.nombre} -> Estado: APAGADO (OFF/0%)")

    def ajustar(self, valor: float):
        if self.tipo_control == "DIGITAL":
            registrar_evento(f"[⚠️ ERROR] {self.nombre} es digital (0/1). Use encender/apagar.")
            return
        if self.rango_operacion_min <= valor <= self.rango_operacion_max:
            self.punto_operacion = valor
            self.estado = valor > 0.0
            registrar_evento(f"[⚙] {self.nombre} -> Modulación: {self.punto_operacion:.1f}%")
        else:
            registrar_evento(f"[⚠️ ERROR] {self.nombre} -> {valor}% fuera de rango (0% - 100%).")

    def info(self) -> str:
        estado_str = "ON" if self.estado else "OFF"
        if self.tipo_control == "DIGITAL":
            return f"{self.nombre:<22} | Tipo: Digital (0/1)  | Estado: {estado_str:<3} | Valor: {int(self.estado)}"
        return f"{self.nombre:<22} | Tipo: Proporcional   | Estado: {estado_str:<3} | Modulación: {self.punto_operacion:>5.1f}%"


class Sensor:
    def __init__(self, nombre: str, variable_fisica: str, rango_min: float, rango_max: float, unidad: str, valor_inicial: float, decimales: int = 2):
        self.nombre = nombre
        self.variable_fisica = variable_fisica
        self.rango_min = rango_min
        self.rango_max = rango_max
        self.unidad = unidad
        self.decimales = decimales
        self.valor_actual = valor_inicial

    def actualizar_valor(self, nuevo_valor: float):
        self.valor_actual = max(self.rango_min, min(self.rango_max, round(nuevo_valor, self.decimales)))

    def leer_valor_actual(self) -> float:
        registrar_evento(f"[📊 LECTURA] {self.nombre}: {self.valor_actual:.{self.decimales}f} {self.unidad}")
        return self.valor_actual

    def info(self) -> str:
        return f"{self.nombre:<20} | Var: {self.variable_fisica:<12} | Medición: {self.valor_actual:>6.2f} {self.unidad:<4} | Rango: [{self.rango_min:.1f} - {self.rango_max:.1f}]"
