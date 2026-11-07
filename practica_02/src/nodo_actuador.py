
import numbers

# Importar la clase padre
from nodo_iot import NodoIoT


class NodoActuador(NodoIoT):
    """
    Clase hija que representa un actuador dentro de una red IoT.
    Hereda de NodoIoT y controla su estado y potencia PWM.
    """

    PWM_MIN = 0
    PWM_MAX = 100

    def __init__(
        self,
        id_dispositivo: str,
        ip: str,
        ubicacion: str,
        tipo: str,
        potencia_pwm: float = 0
    ):

        # Inicializar los atributos heredados
        super().__init__(id_dispositivo, ip, ubicacion)

        # Atributos propios del actuador
        self.tipo = tipo
        self.__estado_activo = False
        self.__potencia_pwm = 0.0

        # Validar la potencia inicial
        self.potencia_pwm = potencia_pwm

    @property
    def estado_activo(self) -> bool:
        """Permite consultar el estado del actuador."""
        return self.__estado_activo

    @property
    def potencia_pwm(self) -> float:
        """Permite consultar la potencia PWM."""
        return self.__potencia_pwm

    @potencia_pwm.setter
    def potencia_pwm(self, valor: float) -> None:
        """
        Valida que la potencia PWM sea un número real
        entre 0 y 100.
        """

        if isinstance(valor, bool) or not isinstance(valor, numbers.Real):
            raise TypeError(
                "Error: La potencia PWM debe ser un número real."
            )

        if not (self.PWM_MIN <= float(valor) <= self.PWM_MAX):
            raise ValueError(
                f"Error: La potencia PWM debe estar entre "
                f"{self.PWM_MIN} y {self.PWM_MAX}."
            )

        self.__potencia_pwm = float(valor)

        # Mantener coherencia entre potencia y estado
        self.__estado_activo = self.__potencia_pwm > 0

    def encender(self, potencia_pwm: float = 100) -> None:
        """Enciende el actuador con la potencia indicada."""

        if isinstance(potencia_pwm, bool) or not isinstance(
            potencia_pwm, numbers.Real
        ):
            raise TypeError(
                "Error: La potencia PWM debe ser un número real."
            )

        if not (0 < float(potencia_pwm) <= self.PWM_MAX):
            raise ValueError(
                f"Error: Para encender, la potencia debe ser "
                f"mayor que 0 y menor o igual a {self.PWM_MAX}."
            )

        self.potencia_pwm = potencia_pwm

        print(
            f"[{self.id_dispositivo}] Actuador encendido "
            f"con potencia PWM de {self.__potencia_pwm}%."
        )

    def apagar(self) -> None:
        """Apaga el actuador y establece su potencia en cero."""

        self.__estado_activo = False
        self.__potencia_pwm = 0.0

        print(f"[{self.id_dispositivo}] Actuador apagado.")

    def enviar_telemetria(self) -> None:
        """
        Sobrescribe el método de la clase padre
        para mostrar información del actuador.
        """

        estado_red = "Conectado" if self.conectado else "Desconectado"

        estado_actuador = (
            "Encendido" if self.__estado_activo else "Apagado"
        )

        print("\n--- Telemetría NodoActuador ---")
        print(
            f"ID: {self.id_dispositivo} | "
            f"IP: {self.ip} | "
            f"Ubicación: {self.ubicacion} ({estado_red})"
        )
        print(f"Tipo de actuador: {self.tipo}")
        print(f"Estado del actuador: {estado_actuador}")
        print(f"Potencia PWM: {self.__potencia_pwm}%")
        print("--------------------------------\n")


# Pruebas de funcionamiento
if __name__ == '__main__':

    print("=== PRUEBAS DE LA CLASE NodoActuador ===")

    # Prueba 1: Crear un actuador
    try:
        print("\n1. Instanciando actuador...")

        actuador1 = NodoActuador(
            "ACT-01",
            "192.168.1.20",
            "Laboratorio",
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
