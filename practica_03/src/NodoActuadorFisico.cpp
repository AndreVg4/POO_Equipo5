#include "NodoActuadorFisico.h"

NodoActuadorFisico::NodoActuadorFisico(
String id,
int pinHardware)
: NodoIoT(id,pinHardware)
{
    estadoActivo=false;
}

void NodoActuadorFisico::setEstado(
bool estado)
{
    estadoActivo=estado;

    digitalWrite(pin,estadoActivo);
}

void NodoActuadorFisico::iniciar()
{
    pinMode(pin,OUTPUT);

    digitalWrite(pin,LOW);

    conectado=true;
}

void NodoActuadorFisico::ejecutarAccion()
{
    digitalWrite(pin,estadoActivo);
}