import os
from collections import deque

from nodo_iot import NodoIoT
from NodoSensor import NodoSensor
from nodo_actuador import NodoActuador


# ==========================================
# GESTIÓN DE PANTALLA Y EVENTOS SCADA
# ==========================================

historial_eventos = deque(maxlen=5)

def limpiar_pantalla():
    """Limpia el búfer de la terminal según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")

def registrar_evento(mensaje: str):
    """Agrega un evento al registro del HMI manteniendo el tamaño acotado."""
    historial_eventos.append(mensaje)


# ==========================================
# CREACIÓN DE LOS DISPOSITIVOS Y RED IoT
# ==========================================

sensor_temp = NodoSensor(
    "SENS-01",
    "192.168.1.10",
    "Invernadero",
    "Temperatura",
    45.5,
    "°C",
    40.0
)

actuador_ventilador = NodoActuador(
    "ACT-01",
    "192.168.1.20",
    "Laboratorio",
    "Ventilador"
)

sensor_luz = NodoSensor(
    "SENS-02",
    "192.168.1.11",
    "Invernadero",
    "Luminosidad",
    65.0,
    "%",
    80.0
)

red_iot = [
    sensor_temp,
    actuador_ventilador,
    sensor_luz
]


# ==========================================
# RENDERIZADO DE LA INTERFAZ HMI
# ==========================================

def mostrar_interfaz_hmi():
    """Dibuja el panel HMI completo con estado de red, nodos e historial."""
    print("=" * 86)
    print("           PANEL HMI - CONTROL Y MONITOREO DE RED IoT MODULAR (v1.0.0)")
    print("=" * 86)
    
    # Resumen de red
    total_nodos = len(red_iot)
    print(f" TOPOLOGÍA: Malla Local | NODOS ACTIVOS: [{total_nodos}] | PROTOCOLO: Telemetría / PWM")
    print("=" * 86)

    # Estado de dispositivos (Polimorfismo / atributos comunes)
    print(" [DISPOSITIVOS CONECTADOS]")
    for dev in red_iot:
        # Se aprovecha si la clase tiene método str/info o sus atributos base
        tipo = dev.__class__.__name__
        id_nodo = getattr(dev, "id_nodo", getattr(dev, "id", "N/A"))
        ip = getattr(dev, "ip", "0.0.0.0")
        ubicacion = getattr(dev, "ubicacion", "N/A")
        
        # Formato tabular limpio
        print(f"   ► [{tipo:<12}] ID: {id_nodo:<8} | IP: {ip:<14} | Ubicación: {ubicacion}")
    print("-" * 86)

    # Historial persistente SCADA
    print(" [HISTORIAL DE EVENTOS SCADA]")
    if not historial_eventos:
        print("   (Sin actividad registrada)")
    else:
        for ev in historial_eventos:
            print(f"   {ev}")
    print("=" * 86)

    # Panel de ayuda de comandos rápidos
    print(" COMANDOS:")
    print("   • conectar                    • telemetria")
    print("   • pwm <1-100> (ventilador)    • apagar")
    print("   • salir")
    print("=" * 86)


# ==========================================
# BUCLE PRINCIPAL DE CONTROL
# ==========================================

def main():
    while True:
        limpiar_pantalla()
        mostrar_interfaz_hmi()

        try:
            entrada = input("HMI >> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[+] Finalizando el sistema IoT...")
            break

        if not entrada:
            continue

        partes = entrada.split()
        cmd = partes[0].lower()

        if cmd == "salir":
            print("\n[+] Finalizando el sistema IoT. ¡Hasta pronto!")
            break

        elif cmd == "conectar":
            for dispositivo in red_iot:
                dispositivo.conectar()
            registrar_evento("[+] Todos los dispositivos han sido sincronizados.")

        elif cmd == "telemetria":
            # Si el método enviar_telemetria() imprime a consola, capturamos el evento
            for dispositivo in red_iot:
                dispositivo.enviar_telemetria()
            registrar_evento("[📡 TELEMETRÍA] Barrido de red completado exitosamente.")

        elif cmd == "pwm":
            if len(partes) > 1:
                try:
                    potencia = float(partes[1])
                    if 1 <= potencia <= 100:
                        actuador_ventilador.encender(potencia)
                        registrar_evento(f"[⚡ ACTUADOR] Ventilador operando a {potencia}% PWM.")
                    else:
                        registrar_evento("[⚠️ ERROR] Rango PWM inválido. Debe ser entre 1 y 100.")
                except ValueError:
                    registrar_evento("[⚠️ ERROR] Ingrese un valor numérico para la potencia.")
            else:
                registrar_evento("[⚠️ ERROR] Sintaxis incorrecta. Uso: pwm <1-100>")

        elif cmd == "apagar":
            actuador_ventilador.apagar()
            registrar_evento("[🛑 ACTUADOR] Ventilador apagado.")

        else:
            registrar_evento(f"[⚠️ ERROR] Comando '{cmd}' no reconocido.")


if __name__ == "__main__":
    main()