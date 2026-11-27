#ifndef NODO_SENSOR_FISICO_H
#define NODO_SENSOR_FISICO_H

#include "NodoIoT.h"

class NodoSensorFisico : public NodoIoT{

private:
    int umbralAlerta;
    int ultimaLectura;

public:

    NodoSensorFisico(
        String id,
        int pinHardware
    );

    void setUmbralAlerta(int valor);

    int getLectura();

    void iniciar() override;

    void ejecutarAccion() override;
};

#endif