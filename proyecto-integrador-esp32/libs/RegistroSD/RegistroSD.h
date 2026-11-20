#ifndef REGISTRO_SD_H
#define REGISTRO_SD_H

#include <SD.h>

#include "RegistroTemperatura.h"

class RegistroSD :
public RegistroTemperatura {

private:

    int pinCS;

public:

    RegistroSD(
        int cs,
        float min,
        float max
    );

    bool begin();

    bool guardar(
        String dato
    ) override;
};

#endif