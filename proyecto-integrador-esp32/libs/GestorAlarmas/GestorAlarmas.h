#ifndef GESTOR_ALARMAS_H
#define GESTOR_ALARMAS_H

class GestorAlarmas {

private:

    int ledVerde;

    int ledRojo;

    int buzzer;

public:

    GestorAlarmas(
        int verde,
        int rojo,
        int buzz
    );

    void begin();

    void normal();

    void alarma();
};

#endif