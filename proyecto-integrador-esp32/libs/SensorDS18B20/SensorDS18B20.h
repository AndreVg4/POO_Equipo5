#ifndef SENSOR_DS18B20_H
#define SENSOR_DS18B20_H

#include <OneWire.h>
#include <DallasTemperature.h>

#include "SensorBase.h"

class SensorDS18B20 : public SensorBase {

private:

    OneWire oneWire;

    DallasTemperature sensor;

    DeviceAddress direccion;

    float temperatura;

public:

    SensorDS18B20(
        uint8_t pin,
        const DeviceAddress addr
    );

    bool begin() override;

    float leer() override;

    float getTemperatura();

    void setTemperatura(float valor);
};

#endif