# Proyecto Integrador ESP32
# Etapa 1 – Propuesta y Arquitectura del Sistema

## Monitoreo de Cadena de Frío para Productos Farmacéuticos y Perecederos

## Información General del Equipo

- **Número de Práctica:** Proyecto Integrador
- **Título del Proyecto:** Monitoreo de Cadena de Frío para Productos Farmacéuticos y Perecederos
- **Fecha de Entrega:** 21/11/2026
- **Enlace al Repositorio de GitHub:** https://github.com/AndreVg4/POO_Equipo5

| Nombre Completo del Integrante | Matrícula UV | Usuario de GitHub |
| :--- | :--- | :--- |
| Andre Vega Morales | S22013537 | @AndreVg4 |
| Ricardo Abraham Sosa Calvario | S22013518 | @RicardoS22 |
| Isaac Vazquez Carrizo | S22013542 | @IsaacVzC |
| Eduardo Ramos Mateos | S22013532 | @Eduardo-Ramoss |
---

# Introducción

La conservación de medicamentos, vacunas y productos perecederos requiere mantener condiciones térmicas controladas durante todo su almacenamiento y transporte. La pérdida de dichas condiciones puede ocasionar daños al producto, pérdida de efectividad y riesgos para la salud.

Para atender esta necesidad se propone el desarrollo de un sistema embebido basado en ESP32 capaz de medir temperatura interna y externa, generar alarmas visuales y sonoras ante condiciones fuera de rango y registrar información en una memoria MicroSD para su posterior análisis.

---

# Objetivo General

Diseñar un sistema embebido para monitorear la temperatura de una cadena de frío mediante sensores digitales DS18B20, utilizando un ESP32 como unidad de procesamiento central.

---

# Objetivos Específicos

- Medir la temperatura interna de un contenedor refrigerado.
- Medir la temperatura ambiente externa.
- Detectar temperaturas fuera de los límites establecidos.
- Generar indicaciones visuales mediante LEDs.
- Generar alarmas acústicas mediante buzzer.
- Almacenar registros de temperatura en una memoria MicroSD.
- Diseñar una arquitectura orientada a objetos para el desarrollo posterior del sistema.

---

# Descripción del Problema

Los productos farmacéuticos y alimenticios requieren mantenerse dentro de rangos específicos de temperatura durante su transporte y almacenamiento.

Cuando la temperatura supera o desciende de los límites establecidos pueden ocurrir problemas tales como:

- Degradación de medicamentos.
- Pérdida de eficacia de vacunas.
- Deterioro de alimentos perecederos.
- Pérdidas económicas.
- Riesgos sanitarios.

Por tal motivo se plantea la implementación de un sistema capaz de monitorear continuamente el estado térmico del sistema de almacenamiento.

---

# Hardware Seleccionado

## Unidad de Procesamiento

### ESP32 DevKit V1

Características principales:

- Microcontrolador de 32 bits.
- WiFi y Bluetooth integrados.
- Compatibilidad con PlatformIO.
- Amplia disponibilidad de GPIO.

---

## Sensores

### DS18B20 Externo

Sensor encargado de medir la temperatura ambiente exterior.

---

### DS18B20 Interno

Sensor encargado de medir la temperatura dentro del contenedor refrigerado.

---

## Actuadores

### LED Verde

Indica que la temperatura se encuentra dentro del rango permitido.

### LED Rojo

Indica una condición de alarma.

### Buzzer Piezoeléctrico

Genera una alerta sonora ante condiciones críticas.

---

## Almacenamiento

### MicroSD SPI

Permite almacenar registros históricos de temperatura en formato CSV.

---

# Variables del Sistema

| Variable | Unidad |
|-----------|----------|
| Temperatura Interna | °C |
| Temperatura Externa | °C |
| Estado de Alarma | Booleano |
| Fecha y Hora del Registro | Timestamp |
| Estado del Sistema | Texto |

---

# Rangos de Operación

Para fines de este proyecto se establece el siguiente rango de operación:

```text
Temperatura mínima: 2 °C

Temperatura máxima: 8 °C
```

Si la temperatura interna se encuentra fuera de estos límites se considerará una condición de alarma.

---

# Arquitectura General del Sistema

El sistema seguirá la siguiente secuencia de funcionamiento:

```text
Adquisición de Temperatura
            ↓
      Procesamiento
            ↓
     Evaluación de Estado
            ↓
       Activación de
        Alarmas
            ↓
      Registro en SD
```

---

# Diagrama de Bloques

```text
      DS18B20 Interno
              |
              |
      DS18B20 Externo
              |
              v
           ESP32
              |
    +---------+---------+
    |         |         |
    v         v         v

 LED Verde LED Rojo Buzzer

              |
              v

          MicroSD
```

---

# UML Inicial


```text

+----------------------+
|   SensorDS18B20      |
+----------------------+
| - pinBus             |
| - temperatura        |
+----------------------+
| + begin()            |
| + leerTemperatura()  |
+----------------------+

+----------------------+
| RegistroTemperatura  |
+----------------------+
| - limiteMinimo       |
| - limiteMaximo       |
+----------------------+
| + guardarRegistro()  |
| + verificarRango()   |
+----------------------+

+----------------------+
|   GestorAlarmas      |
+----------------------+
| - ledVerde           |
| - ledRojo            |
| - buzzer             |
+----------------------+
| + normal()           |
| + alarma()           |
+----------------------+

+----------------------+
|   CadenaFrioESP32    |
+----------------------+
| - sensorInterno      |
| - sensorExterno      |
| - registro           |
| - alarmas            |
+----------------------+
| + begin()            |
| + actualizar()       |
+----------------------+


```

Propuesta inicial de clases:

```text
SensorBase

SensorDS18B20

RegistroTemperatura

GestorAlarmas

CadenaFrioESP32
```

Relación preliminar:

```text
SensorBase
      |
      |
SensorDS18B20

CadenaFrioESP32
      |
      +---- RegistroTemperatura
      |
      +---- GestorAlarmas
```

---

# Esquema de Conexión


```text
diagrams/esquema_conexion.png
```

Asignación preliminar de pines:

| Dispositivo | GPIO ESP32 |
|------------|------------|
| Bus OneWire DS18B20 | GPIO4 |
| LED Verde | GPIO26 |
| LED Rojo | GPIO27 |
| Buzzer | GPIO25 |
| SD CS | GPIO5 |
| SD MOSI | GPIO23 |
| SD MISO | GPIO19 |
| SD SCK | GPIO18 |

---

# Estructura Inicial del Repositorio

```text
Proyecto_integrador_POO/

├── docs/
│
├── diagrams/
│
├── src/
│
├── platformio.ini
│
└── README.md
```

---

# Resultados Esperados

Se espera obtener un sistema capaz de:

- Monitorear temperaturas internas y externas.
- Diferenciar condiciones normales y de alarma.
- Proporcionar alertas visuales y sonoras.
- Registrar información histórica en almacenamiento externo.
- Servir como base para la implementación de Programación Orientada a Objetos en etapas posteriores.

---

# Conclusiones

Durante esta etapa se definió la arquitectura general del sistema de monitoreo de cadena de frío, así como el hardware requerido y la estructura de software que será utilizada durante el desarrollo del proyecto.

La propuesta permite abordar un problema real de supervisión térmica mediante una solución modular basada en ESP32, estableciendo las bases necesarias para la implementación de una arquitectura orientada a objetos en la siguiente etapa del proyecto.