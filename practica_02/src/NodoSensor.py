import numbers

# Para importar la clase padre
try:
    from nodo_iot import NodoIoT
except ImportError:
    # Dummy de la clase padre únicamente para ejecutar pruebas locales
    class NodoIoT:
        def __init__(self, id_dispositivo: str, ip: str, ubicacion: str, conectado: bool = False):
            self.id_dispositivo = id_dispositivo
            self.ip = ip
            self.ubicacion = ubicacion
            self.conectado = conectado
        def enviar_telemetria(self):
            pass

class NodoSensor(NodoIoT):
    """
    Clase hija que representa un sensor (ej. temperatura o luz).
    Hereda de NodoIoT y maneja un límite de alerta validado.
    """
    
    # Rangos de temperatura, p.e.
    RANGO_MIN = -20.0
    RANGO_MAX = 100.0

    def __init__(self, id_dispositivo: str, ip: str, ubicacion: str, tipo: str, lectura_actual: float, unidad: str, limite_alerta: float):
        super().__init__(id_dispositivo, ip, ubicacion)
        
        # Atributos propios del sensor
        self.tipo = tipo
        self.lectura_actual = lectura_actual
        self.unidad = unidad
 
        self.__limite_alerta = None
        self.limite_alerta = limite_alerta 

    @property
    def limite_alerta(self) -> float:
        return self.__limite_alerta

    @limite_alerta.setter
    def limite_alerta(self, valor: float) -> None:
        if isinstance(valor, bool) or not isinstance(valor, numbers.Real):
            raise TypeError(f"Error: El límite debe ser un número real. Se rechazó el tipo '{type(valor).__name__}'.")
        if not (self.RANGO_MIN <= float(valor) <= self.RANGO_MAX):
            raise ValueError(f"Error: Límite {valor} fuera de rango. Debe estar entre {self.RANGO_MIN} y {self.RANGO_MAX} {self.unidad}.")
        
        self.__limite_alerta = float(valor)

    def enviar_telemetria(self) -> None:
        estado_red = "Conectado" if self.conectado else "Desconectado"
        alerta = "¡ALERTA SUPERADA!" if self.lectura_actual > self.__limite_alerta else "Lectura estable"
        
        print("\n--- Telemetría NodoSensor ---")
        print(f"ID: {self.id_dispositivo} | IP: {self.ip} | Ubicación: {self.ubicacion} ({estado_red})")
        print(f"Sensor: {self.tipo} | Lectura: {self.lectura_actual} {self.unidad}")
        print(f"Límite configurado: {self.__limite_alerta} {self.unidad} -> Estado: {alerta}")
        print("-----------------------------\n")

if __name__ == '__main__':
    print("=== PRUEBAS DE LA CLASE NodoSensor ===")
    
    # Prueba 1: Se crea un sensor con atributos comunes y específicos (Límite válido se acepta)
    try:
        print("\n1. Instanciando sensor válido...")
        sensor1 = NodoSensor("SENS-01", "192.168.1.10", "Invernadero 1", "Temperatura", 45.5, "°C", 40.0)
        sensor1.conectado = True 
        sensor1.enviar_telemetria() 
        print("-> Prueba 1 exitosa.")
    except Exception as e:
        print(f"Error inesperado: {e}")

    # Prueba 2: Se rechazan valores fuera del rango
    try:
        print("\n2. Probando límite fuera de rango (150.0 °C)...")
        sensor2 = NodoSensor("SENS-02", "192.168.1.11", "Planta Baja", "Temperatura", 25.0, "°C", 150.0)
    except ValueError as e:
        print(f"-> Excepción capturada correctamente: {e}")

    # Prueba 3: Se rechaza texto
    try:
        print("\n3. Probando límite tipo texto ('ochenta')...")
        sensor3 = NodoSensor("SENS-03", "192.168.1.12", "Laboratorio", "Temperatura", 25.0, "°C", "ochenta")
    except TypeError as e:
        print(f"-> Excepción capturada correctamente: {e}")

    # Prueba 4: Se rechazan booleanos
    try:
        print("\n4. Probando límite tipo booleano (True)...")
        sensor4 = NodoSensor("SENS-04", "192.168.1.13", "Exterior", "Temperatura", 25.0, "°C", True)
    except TypeError as e:
        print(f"-> Excepción capturada correctamente: {e}")