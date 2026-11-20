#ifndef REGISTRO_TEMP_H
#define REGISTRO_TEMP_H

#include <Arduino.h>

class RegistroTemperatura {

protected:

    float limiteInferior;

    float limiteSuperior;

public:

    RegistroTemperatura(
        float min,
        float max
    );

    virtual bool guardar(
        String dato
    ) = 0;

    virtual ~RegistroTemperatura(){}
};

#endif