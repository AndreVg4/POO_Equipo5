+------------------------------------------+
|              NodoActuador               |
+------------------------------------------+
| - __estado_activo: bool                  |
| - __potencia_pwm: float                  |
| + tipo: str                              |
| + PWM_MIN: int                           |
| + PWM_MAX: int                           |
+------------------------------------------+
| + __init__(id_dispositivo: str,          |
|   ip: str, ubicacion: str,               |
|   tipo: str, potencia_pwm: float = 0)    |
|                                          |
| + estado_activo: bool                    |
| + potencia_pwm: float                    |
| + encender(potencia_pwm: float = 100):   |
|   None                                   |
| + apagar(): None                         |
| + enviar_telemetria(): None              |
+------------------------------------------+
