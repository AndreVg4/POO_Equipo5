"""
EE: Programación Orientada a Objetos 
Versión 1.0.0: Simulador de Reactor Químico en Python
Lazo cerrado térmico/barométrico con HMI estático e Interlocks de seguridad.
"""

import os
import random

# ==============================================================================
#                    GESTOR DE EVENTOS Y TERMINAL
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

# ==============================================================================
                 #LÓGICA DINÁMICA, LAZO CERRADO E INTERLOCKS
# ==============================================================================
class ReactorQuimico:
    def __init__(self):
        self.sensor_temp = Sensor("Sensor Temperatura", "Temperatura", 0.0, 150.0, "°C", valor_inicial=72.0)
        self.sensor_pres = Sensor("Sensor Presión", "Presión", 0.0, 15.0, "Bar", valor_inicial=7.5)

        self.bomba_enfriamiento = Actuador("Bomba de Enfriamiento", tipo_control="PROPORCIONAL")
        self.valvula_alivio = Actuador("Válvula de Alivio", tipo_control="DIGITAL")

        self.modo_operacion = "MANUAL"
        self.interlock_activo = False

    def verificar_interlocks(self) -> bool:
        if self.sensor_temp.valor_actual > 85.0 or self.sensor_pres.valor_actual > 12.0:
            self.interlock_activo = True
            self.bomba_enfriamiento.ajustar(100.0)
            self.valvula_alivio.encender()
            registrar_evento("[🚨 INTERLOCK CRÍTICO] T>85°C o P>12 Bar. Bomba forzada a 100% y Alivio ABIERTO.")
            return True
        self.interlock_activo = False
        return False

    def paso_simulacion(self):
        if self.modo_operacion == "AUTOMATICO":
            if self.sensor_temp.valor_actual > 75.0:
                self.bomba_enfriamiento.ajustar(85.0)
            elif self.sensor_temp.valor_actual < 65.0:
                self.bomba_enfriamiento.ajustar(15.0)
            else:
                self.bomba_enfriamiento.ajustar(35.0)

        delta_t = 1.5 - (0.05 * self.bomba_enfriamiento.punto_operacion)
        ruido = random.uniform(-0.08, 0.08)
        self.sensor_temp.actualizar_valor(self.sensor_temp.valor_actual + delta_t + ruido)

        delta_p = delta_t * 0.07
        if self.valvula_alivio.estado:
            delta_p -= 1.0
        self.sensor_pres.actualizar_valor(self.sensor_pres.valor_actual + delta_p)

        self.verificar_interlocks()

    def inyectar_fallo(self):
        fallo = random.choice(["termico", "presion"])
        if fallo == "termico":
            self.sensor_temp.actualizar_valor(93.0)
            registrar_evento("[⚡ TEST FALLO] Sobrecalentamiento inducido: 93.0 °C")
        else:
            self.sensor_pres.actualizar_valor(13.5)
            registrar_evento("[⚡ TEST FALLO] Sobrepresión inducida: 13.5 Bar")
        self.verificar_interlocks()


# ==============================================================================
                  INTERFAZ HMI Y BUCLE PRINCIPAL
# =============================================================================
def mostrar_interfaz_hmi(reactor: ReactorQuimico):
    print("=" * 86)
    print("           PANEL HMI - CONTROL Y MONITOREO DE REACTOR QUÍMICO (v1.0.0)")
    print("=" * 86)
    estado_seg = "🚨 ENCLAVAMIENTO (BLOQUEO)" if reactor.interlock_activo else "🟢 NORMAL"
    print(f" MODO OPERATIVO: [{reactor.modo_operacion:<10}] | SISTEMA DE SEGURIDAD: [{estado_seg}]")
    print("=" * 86)

    print(" [SENSORES ANALÓGICOS]")
    print(f"   ► [temp]    {reactor.sensor_temp.info()}")
    print(f"   ► [presion] {reactor.sensor_pres.info()}")
    print("-" * 86)

    print(" [ACTUADORES DE CONTROL]")
    print(f"   ► [bomba]   {reactor.bomba_enfriamiento.info()}")
    print(f"   ► [valvula] {reactor.valvula_alivio.info()}")
    print("=" * 86)

    print(" [HISTORIAL DE EVENTOS SCADA]")
    if not historial_eventos:
        print("   (Sin actividad registrada)")
    else:
        for ev in historial_eventos:
            print(f"   {ev}")
    print("=" * 86)

    print(" COMANDOS:")
    print("   • modo <manual/auto/pruebas>   • ajustar bomba <0-100>")
    print("   • encender/apagar <actuador>   • leer <temp/presion>")
    print("   • paso (avanza 1 ciclo físico) • terminar")
    print("=" * 86)


def main():
    reactor = ReactorQuimico()
    sensores = {"temp": reactor.sensor_temp, "presion": reactor.sensor_pres}
    actuadores = {"bomba": reactor.bomba_enfriamiento, "valvula": reactor.valvula_alivio}

    while True:
        limpiar_pantalla()
        mostrar_interfaz_hmi(reactor)

        try:
            entrada = input("HMI >> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[+] Saliendo del simulador.")
            break

        if not entrada:
            continue

        if entrada.lower() == "terminar":
            print("\n[+] Simulador cerrado correctamente.")
            break

        partes = entrada.split()
        cmd = partes[0].lower()

        if cmd == "modo":
            if len(partes) > 1:
                seleccion = partes[1].lower()
                if seleccion in ["manual", "man"]:
                    reactor.modo_operacion = "MANUAL"
                    registrar_evento("[+] Modo Manual activado.")
                elif seleccion in ["auto", "automatico"]:
                    reactor.modo_operacion = "AUTOMATICO"
                    registrar_evento("[+] Modo Automático activado (Lazo cerrado).")
                elif seleccion in ["pruebas", "test"]:
                    reactor.modo_operacion = "PRUEBAS"
                    reactor.inyectar_fallo()
            else:
                registrar_evento("[⚠️ ERROR] Especifique el modo: modo <manual/auto/pruebas>")

        elif cmd == "paso":
            reactor.paso_simulacion()
            registrar_evento("[⏱ CICLO] Simulación dinámica ejecutada.")

        elif cmd == "leer":
            if len(partes) > 1 and partes[1].lower() in sensores:
                sensores[partes[1].lower()].leer_valor_actual()
            else:
                registrar_evento("[⚠️ ERROR] Sensor no válido. Opciones: temp, presion")

        elif cmd == "ajustar":
            if reactor.interlock_activo:
                registrar_evento("[🚫 DENEGADO] Interlock activo. Control manual bloqueado.")
                continue
            if len(partes) >= 3 and partes[1].lower() in actuadores:
                try:
                    valor = float(partes[2])
                    actuadores[partes[1].lower()].ajustar(valor)
                except ValueError:
                    registrar_evento("[⚠️ ERROR] Ingrese un valor numérico.")
            else:
                registrar_evento("[⚠️ ERROR] Uso: ajustar bomba <0-100>")

        elif cmd in ["encender", "apagar"]:
            if reactor.interlock_activo:
                registrar_evento("[🚫 DENEGADO] Interlock activo. Control manual bloqueado.")
                continue
            if len(partes) > 1 and partes[1].lower() in actuadores:
                act = actuadores[partes[1].lower()]
                act.encender() if cmd == "encender" else act.apagar()
            else:
                registrar_evento(f"[⚠️ ERROR] Uso: {cmd} <bomba/valvula>")

        else:
            registrar_evento(f"[⚠️ ERROR] Comando '{cmd}' desconocido.")

        reactor.paso_simulacion()


if __name__ == "__main__":
    main()
