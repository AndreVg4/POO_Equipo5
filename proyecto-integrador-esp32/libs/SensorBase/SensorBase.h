#ifndef SENSOR_BASE_H
#define SENSOR_BASE_H

class SensorBase {

public:

    virtual bool begin() = 0;

    virtual float leer() = 0;

    virtual ~SensorBase() {}
};

#endif