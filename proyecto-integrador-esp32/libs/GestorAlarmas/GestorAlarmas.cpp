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

void GestorAlarmas::ajustarPWM(int valor) //Nuevo método para regular la potencia de buzzer
{
    valor=constrain(valor, 0, 255);
    analogWrite(buzzer, valor)
}
