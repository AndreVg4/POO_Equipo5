#ifndef NODO_ACTUADOR_FISICO_H
#define NODO_ACTUADOR_FISICO_H

#include "NodoIoT.h"

class NodoActuadorFisico : public NodoIoT{

private:
    bool estadoActivo;

public:

    NodoActuadorFisico(
        String id,
        int pinHardware
    );

    void setEstado(bool estado);

    void iniciar() override;

    void ejecutarAccion() override;
};

#endif