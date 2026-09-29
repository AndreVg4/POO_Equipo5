#include <OneWire.h>
#include <DallasTemperature.h>

// ============================================================================
// CLASE 1: ACTUADOR PWM 
// ============================================================================
class ActuadorPWM {
  private:
    int _pin;
    int _freq;
    int _resolucion;
    int _dutyActual;

  public:
    ActuadorPWM(int pin, int freq = 5000, int resolucion = 8)
      : _pin(pin), _freq(freq), _resolucion(resolucion), _dutyActual(0) {}

    void inicializar() {
      ledcAttach(_pin, _freq, _resolucion);
      escribirPWM(0);
    }

    void escribirPWM(int duty) {
      _dutyActual = constrain(duty, 0, 255);
      ledcWrite(_pin, _dutyActual);
    }

    int obtenerDuty() const {
      return _dutyActual;
    }
};

// ============================================================================
// CLASE 2: SENSOR LDR 
// ============================================================================
class SensorLDR {
  private:
    int _pin;

  public:
    SensorLDR(int pin) : _pin(pin) {}

    void inicializar() {
      analogReadResolution(12);
    }

    int leerLuz() const {
      return analogRead(_pin); // Retorna 0 - 4095
    }

    // Calcula el duty inverso proporcional (0 a 255)
    int calcularPWMInverso() const {
      int adc = leerLuz();
      int pwm = map(adc, 0, 4095, 255, 0);
      return constrain(pwm, 0, 255);
    }
};

// ============================================================================
// CLASE 3: SENSOR TÉRMICO DIGITAL
// ============================================================================
class SensorTermicoDS18B20 {
  private:
    int _pin;
    OneWire _oneWire;
    DallasTemperature _sensor;

  public:
    SensorTermicoDS18B20(int pin)
      : _pin(pin), _oneWire(pin), _sensor(&_oneWire) {}

    void inicializar() {
      _sensor.begin();
    }

    float leerTemperatura() {
      _sensor.requestTemperatures();
      float temp = _sensor.getTempCByIndex(0);
      return (temp == DEVICE_DISCONNECTED_C) ? 0.0 : temp;
    }
};

// ============================================================================
// CLASE 4: CONTROLADOR DE PLANTA 
// ============================================================================
class ControladorPlanta {
  private:
    SensorTermicoDS18B20 _sensorTemp;
    SensorLDR _sensorLuz;
    ActuadorPWM _ventilador;
    ActuadorPWM _led;

    bool _modoManual;
    int _manualPWMVent;
    int _manualPWMLED;

  public:
    ControladorPlanta(int pinTemp, int pinLDR, int pinVent, int pinLED)
      : _sensorTemp(pinTemp),
        _sensorLuz(pinLDR),
        _ventilador(pinVent, 5000, 8),
        _led(pinLED, 5000, 8),
        _modoManual(false),
        _manualPWMVent(0),
        _manualPWMLED(0) {}

    void inicializar() {
      _sensorTemp.inicializar();
      _sensorLuz.inicializar();
      _ventilador.inicializar();
      _led.inicializar();
    }

    void actualizar() {
      float temp = _sensorTemp.leerTemperatura();
      int luz = _sensorLuz.leerLuz();

      int pwmVent = 0;
      int pwmLED = 0;

      if (_modoManual) {
        pwmVent = _manualPWMVent;
        pwmLED = _manualPWMLED;
      } else {
        // Regla térmica: 100% (255) si excede 30 °C
        pwmVent = (temp > 30.0) ? 255 : 0;

        // Regla lumínica: Proporcional inversa
        pwmLED = _sensorLuz.calcularPWMInverso();
      }

      // Aplicar a los objetos actuadores
      _ventilador.escribirPWM(pwmVent);
      _led.escribirPWM(pwmLED);

      // Emitir telemetría estructurada
      enviarTelemetria(temp, luz);
    }

    void procesarComando(const String &comando) {
      if (comando.equalsIgnoreCase("AUTO")) {
        _modoManual = false;
        Serial.println("{\"status\": \"Modo AUTO activado\"}");
      } else if (comando.startsWith("VENT:")) {
        _modoManual = true;
        _manualPWMVent = constrain(comando.substring(5).toInt(), 0, 255);
        Serial.println("{\"status\": \"Ventilador forzado\"}");
      } else if (comando.startsWith("LED:")) {
        _modoManual = true;
        _manualPWMLED = constrain(comando.substring(4).toInt(), 0, 255);
        Serial.println("{\"status\": \"LED forzado\"}");
      }
    }

  private:
    void enviarTelemetria(float temp, int luz) {
      Serial.print("{\"temperatura\": ");
      Serial.print(temp, 1);
      Serial.print(", \"luz\": ");
      Serial.print(luz);
      Serial.print(", \"pwm_ventilador\": ");
      Serial.print(_ventilador.obtenerDuty());
      Serial.print(", \"pwm_led\": ");
      Serial.print(_led.obtenerDuty());
      Serial.print(", \"modo\": \"");
      Serial.print(_modoManual ? "MANUAL" : "AUTO");
      Serial.println("\"}");
    }
};

// ============================================================================
// INSTANCIACIÓN Y PUNTO DE ENTRADA ARDUINO
// ============================================================================
// Asignación de pines: DS18B20=GPIO4, LDR=GPIO32, Vent=GPIO18, LED=GPIO19
ControladorPlanta planta(4, 32, 18, 19);

void setup() {
  Serial.begin(115200);
  planta.inicializar();
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    planta.procesarComando(cmd);
  }

  planta.actualizar();
  delay(1000);
}