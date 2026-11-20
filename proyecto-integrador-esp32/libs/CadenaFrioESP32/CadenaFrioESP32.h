#ifndef CADENA_FRIO_H
#define CADENA_FRIO_H

#include "SensorDS18B20.h"
#include "RegistroSD.h"
#include "GestorAlarmas.h"

class CadenaFrioESP32 {

private:

    SensorDS18B20 sensorInterno;

    SensorDS18B20 sensorExterno;

    RegistroSD registro;

    GestorAlarmas alarmas;

public:

    CadenaFrioESP32();

    void begin();

    void actualizar();
};

#endif