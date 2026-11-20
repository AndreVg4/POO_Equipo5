# Diagramas del Proyecto

Esta carpeta contiene los diagramas, evidencias visuales y recursos gráficos utilizados durante el desarrollo del proyecto:

# Monitoreo de Cadena de Frío para Productos Farmacéuticos y Perecederos

## Contenido

### uml_clases_inicial.png

Diagrama UML correspondiente a la Etapa 1.

Representa la arquitectura propuesta del sistema antes de la implementación de los principios de Programación Orientada a Objetos.

Incluye las clases:

- SensorDS18B20
- RegistroTemperatura
- GestorAlarmas
- CadenaFrioESP32

---

### uml_clases_v2.png

Diagrama UML correspondiente a la Etapa 2.

Representa la arquitectura final implementada en el proyecto utilizando Programación Orientada a Objetos.

Incluye:

- Herencia
- Encapsulamiento
- Polimorfismo
- Modularización del código

Clases implementadas:

- SensorBase
- SensorDS18B20
- RegistroTemperatura
- RegistroSD
- GestorAlarmas
- CadenaFrioESP32

---

### esquema_conexion.png

Esquema de conexión física del hardware.

Componentes principales:

- ESP32 DevKit V1
- Sensor DS18B20 Interno
- Sensor DS18B20 Externo
- Resistencia Pull-Up 4.7 kΩ
- LED Verde
- LED Rojo
- Buzzer Piezoeléctrico
- Módulo MicroSD SPI

---

### monitor_serial.png

Captura del monitor serial mostrando el funcionamiento del sistema.

Ejemplo de salida:

```text
Interna: 7.12 °C
Externa: 23.56 °C
```

---

### pruebas_unitarias.png

Captura de la ejecución de pruebas unitarias mediante Unity y PlatformIO.

Resultado esperado:

```text
3 test cases: 3 succeeded
```

---

### hardware.jpg

Fotografía del montaje físico del proyecto.

La imagen debe mostrar:

- ESP32
- Sensores DS18B20
- LEDs
- Buzzer
- Módulo MicroSD

Junto con una nota manuscrita que incluya:

- Fecha
- Número de práctica
- Matrículas de los integrantes

---

## Herramientas Utilizadas

- Mermaid
- Draw.io (diagrams.net)
- PlatformIO
- Visual Studio Code

---

## Estructura de la Carpeta

```text
diagrams/

├── README.md
├── UML_Etapa1.png
├── UML_Etapa2.png
├── Diagrama_Conexiones.png
├── monitor_serial.png
├── pruebas_unitarias.png
└── hardware.jpg
```
