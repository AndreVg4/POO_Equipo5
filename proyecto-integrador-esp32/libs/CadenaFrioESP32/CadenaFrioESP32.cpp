#include <Arduino.h>

#include "CadenaFrioESP32.h"
#include "ConfigHardware.h"

DeviceAddress sensorExternoAddr =
{
    0x28, 0xC0, 0xB7, 0xB1,
    0x00, 0x00, 0x00, 0x81
};

DeviceAddress sensorInternoAddr =
{
    0x28, 0xFF, 0xE5, 0x33,
    0x62, 0x14, 0x03, 0x5F
};

CadenaFrioESP32::CadenaFrioESP32()
:

sensorInterno(
    PIN_ONEWIRE,
    sensorInternoAddr
),

sensorExterno(
    PIN_ONEWIRE,
    sensorExternoAddr
),
registro(
    SD_CS,
    TEMP_MINIMA,
    TEMP_MAXIMA
),
alarmas(
    LED_VERDE,
    LED_ROJO,
    BUZZER_PIN
)
{

}

void CadenaFrioESP32::begin()
{
    sensorInterno.begin();

    sensorExterno.begin();

    registro.begin();

    alarmas.begin();
}

void CadenaFrioESP32::actualizar()
{
    float tInterna =
        sensorInterno.leer();

    float tExterna =
        sensorExterno.leer();

    String linea =
        String(tInterna)
        + ","
        + String(tExterna);

    registro.guardar(linea);

    if(
        tInterna < TEMP_MINIMA ||
        tInterna > TEMP_MAXIMA
    )
    {
        alarmas.alarma();
    }
    else
    {
        alarmas.normal();
    }

    Serial.print(
        "Interna: "
    );

    Serial.print(
        tInterna
    );

    Serial.print(
        " Externa: "
    );

    Serial.println(
        tExterna
    );
}