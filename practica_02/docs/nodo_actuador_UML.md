
+--------------------------------------+
|             NodoActuador             |
+--------------------------------------+
| - __estado_activo: bool              |
| - __potencia_pwm: float              |
| + tipo: str                          |
| + PWM_MIN: int                       |
| + PWM_MAX: int                       |
+--------------------------------------+
| + __init__(id_dispositivo, ip,       |
|   ubicacion, tipo, potencia_pwm):    |
|   None                               |
| + estado_activo: bool                |
| + potencia_pwm: float                |
| + encender(potencia_pwm=100): None   |
| + apagar(): None                     |
| + enviar_telemetria(): None          |
+--------------------------------------+
