#ifndef NODO_IOT_H
#define NODO_IOT_H

#include <Arduino.h>

class NodoIoT{
protected:
    String idDispositivo;
    int pin;
    bool conectado;

public:
    NodoIoT(String id,int pinHardware)
        : idDispositivo(id),
          pin(pinHardware),
          conectado(false){}

    virtual void iniciar() = 0;
    virtual void ejecutarAccion() = 0;

    virtual ~NodoIoT(){}
};

#endif