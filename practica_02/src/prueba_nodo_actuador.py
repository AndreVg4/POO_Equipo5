
from nodo_actuador import NodoActuador

# Pruebas de funcionamiento
if __name__ == '__main__':

    print("=== PRUEBAS DE LA CLASE NodoActuador ===")

    # Prueba 1: Crear un actuador
    try:
        print("\n1. Instanciando actuador...")

        actuador1 = NodoActuador(
            "IIE001",
            "192.168.1.20",
            "salon C-001",
            "Ventilador"
        )

        actuador1.conectado = True
        actuador1.enviar_telemetria()

        print("-> Prueba 1 exitosa.")

    except Exception as e:
        print(f"Error inesperado: {e}")

    # Prueba 2: Encender el actuador
    try:
        print("\n2. Encendiendo actuador con PWM de 75%...")

        actuador1.encender(75)
        actuador1.enviar_telemetria()

        print("-> Prueba 2 exitosa.")

    except Exception as e:
        print(f"Error inesperado: {e}")

    # Prueba 3: Apagar el actuador
    try:
        print("\n3. Apagando actuador...")

        actuador1.apagar()
        actuador1.enviar_telemetria()

        print("-> Prueba 3 exitosa.")

    except Exception as e:
        print(f"Error inesperado: {e}")

    # Prueba 4: Rechazar potencia fuera de rango
    try:
        print("\n4. Probando PWM fuera de rango (150)...")

        actuador1.encender(150)

    except ValueError as e:
        print(f"-> Excepción capturada correctamente: {e}")

    # Prueba 5: Rechazar texto
    try:
        print("\n5. Probando PWM con texto...")

        actuador1.encender("alto")

    except TypeError as e:
        print(f"-> Excepción capturada correctamente: {e}")

    # Prueba 6: Rechazar booleanos
    try:
        print("\n6. Probando PWM con booleano (True)...")

        actuador1.encender(True)

    except TypeError as e:
        print(f"-> Excepción capturada correctamente: {e}")

    print("\n=== FIN DE LAS PRUEBAS ===")
