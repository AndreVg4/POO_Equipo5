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
),
alarmaForzada(false)
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
        alarmaForzada ||
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

void CadenaFrioESP32::procesarComando(Srting comando)
{
    comando.trim();
    if (comando == "ALARMA_ON"){
        alarmaForzada = true;
        alarmas.alarma();
        Serial.println("Alarma activda manualmente");
    }
    else if (comando == "ALARMA_OFF"){
        alarmaForzada = false;
        alarmas.normal();
        Serial.println("Alarma normalizada");
    }
    else if (comando.startsWith("PWM")){
        int pwmVal = comando.substring(4).toInt();
        alarmas.ajustarPWM(pwmVal);
        Serial.print("PWM ajustado a ");
        Serial.println(pwmVal);
    }
}
