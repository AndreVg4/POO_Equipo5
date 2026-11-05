```mermaid
classDiagram
    class NodoSensor {
        + RANGO_MIN: float = -20.0
        + RANGO_MAX: float = 100.0
        -__limite_alerta : float
        +tipo : str
        +lectura_actual : float
        +unidad : str
        +__init__(id_dispositivo, ip, ubicacion, tipo, lectura, unidad, limite) None
        +limite_alerta(valor: float) None
        +limite_alerta() float
        +enviar_telemetria() None
    }
```
