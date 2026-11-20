#include "RegistroSD.h"

RegistroSD::RegistroSD(
int cs,
float min,
float max)
:
RegistroTemperatura(min,max)
{
    pinCS = cs;
}

bool RegistroSD::begin()
{
    return SD.begin(pinCS);
}

bool RegistroSD::guardar(
String dato)
{
    File archivo =
        SD.open(
            "/temperaturas.csv",
            FILE_APPEND
        );

    if(!archivo)
        return false;

    archivo.println(dato);

    archivo.close();

    return true;
}