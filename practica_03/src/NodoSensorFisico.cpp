#include "NodoSensorFisico.h"

NodoSensorFisico::NodoSensorFisico(
String id,
int pinHardware)
: NodoIoT(id,pinHardware)
{
    umbralAlerta = 2000;
}

void NodoSensorFisico::setUmbralAlerta(
int valor)
{
    if(valor >= 0 && valor <= 4095)
    {
        umbralAlerta = valor;
    }
}

int NodoSensorFisico::getLectura()
{
    return ultimaLectura;
}

void NodoSensorFisico::iniciar()
{
    pinMode(pin,INPUT);
    conectado=true;
}

void NodoSensorFisico::ejecutarAccion()
{
    ultimaLectura = analogRead(pin);

    Serial.print(idDispositivo);
    Serial.print(": ");

    Serial.println(ultimaLectura);
}