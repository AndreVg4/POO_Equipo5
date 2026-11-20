#include "SensorDS18B20.h"

SensorDS18B20::SensorDS18B20(uint8_t pin, const DeviceAddress addr)
:
oneWire(pin),
sensor(&oneWire)
{
memcpy(
        direccion,
        addr,
        sizeof(DeviceAddress)
    );

    temperatura = 0;
}

bool SensorDS18B20::begin()
{
    sensor.begin();
    return true;
}

float SensorDS18B20::leer()
{
    sensor.requestTemperatures();

     temperatura =
        sensor.getTempC(
            direccion
        );
    return temperatura;
}

float SensorDS18B20::getTemperatura()
{
    return temperatura;
}

void SensorDS18B20::setTemperatura(float valor)
{
    temperatura = valor;
}