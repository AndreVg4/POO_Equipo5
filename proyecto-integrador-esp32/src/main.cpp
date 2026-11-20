#include <Arduino.h>

#include "CadenaFrioESP32.h"

CadenaFrioESP32 sistema;

void setup()
{
    Serial.begin(115200);

    sistema.begin();
}

void loop()
{
    static unsigned long ultimo = 0;

    if(
        millis() - ultimo
        >= 5000
    )
    {
        sistema.actualizar();

        ultimo = millis();
    }
}