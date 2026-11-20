#include <Arduino.h>

#include "GestorAlarmas.h"

GestorAlarmas::GestorAlarmas(
int verde,
int rojo,
int buzz)
{
    ledVerde = verde;
    ledRojo = rojo;
    buzzer = buzz;
}

void GestorAlarmas::begin()
{
    pinMode(
        ledVerde,
        OUTPUT
    );

    pinMode(
        ledRojo,
        OUTPUT
    );

    pinMode(
        buzzer,
        OUTPUT
    );
}

void GestorAlarmas::normal()
{
    digitalWrite(ledVerde,HIGH);
    digitalWrite(ledRojo,LOW);
    digitalWrite(buzzer,LOW);
}

void GestorAlarmas::alarma()
{
    digitalWrite(ledVerde,LOW);
    digitalWrite(ledRojo,HIGH);
    digitalWrite(buzzer,HIGH);
}