import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import serial
import serial.tools.list_ports
import threading
import re
from datetime import datetime


class ComunicacionSerial:
    """Encapsula la comunicación UART bidireccional con el ESP32."""
    def __init__(self, al_recibir_lectura, al_recibir_evento):
        self.serial_conn = None
        self.conectado = False
        self.hilo = None
        self.al_recibir_lectura = al_recibir_lectura
        self.al_recibir_evento = al_recibir_evento

    def obtener_puertos(self):
        return [p.device for p in serial.tools.list_ports.comports()]

    def conectar(self, puerto, baudrate=115200):
        try:
            self.serial_conn = serial.Serial(puerto, baudrate, timeout=1)
            self.conectado = True
            self.hilo = threading.Thread(target=self._bucle_lectura, daemon=True)
            self.hilo.start()
            return True
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a {puerto}:\n{e}")
            return False

    def desconectar(self):
        self.conectado = False
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()

    def enviar(self, comando):
        if self.conectado and self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.write(f"{comando}\n".encode("utf-8"))
            self.al_recibir_evento(f"[PC -> ESP32] {comando}")
        else:
            self.al_recibir_evento("[AVISO] Puerto desconectado. No se envió el comando.")

    def _bucle_lectura(self):
        while self.conectado:
            try:
                if self.serial_conn.in_waiting > 0:
                    linea = self.serial_conn.readline().decode("utf-8", errors="ignore").strip()
                    if linea:
                        self._interpretar_trama(linea)
            except Exception as e:
                if self.conectado:
                    self.al_recibir_evento(f"[ERROR DE LECTURA] {e}")
                break

    def _interpretar_trama(self, linea):
        # Coincidencias con Serial.print("Interna") y Serial.print("Externa")
        patron = r"Interna:\s*([-+]?\d*\.\d+|\d+)\s*Externa:\s*([-+]?\d*\.\d+|\d+)"
        coincidencia = re.search(patron, linea)
        if coincidencia:
            t_interna = float(coincidencia.group(1))
            t_externa = float(coincidencia.group(2))
            self.al_recibir_lectura(t_interna, t_externa)
        else:
            self.al_recibir_evento(f"[ESP32 -> PC] {linea}")


class DashboardHMI:
    """Clase principal de la interfaz gráfica HMI con Tkinter."""
    def __init__(self, root):
        self.root = root
        self.root.title("HMI Cadena de Frío - ESP32")
        self.root.geometry("800x560")
        self.root.configure(bg="#181824")

        # Límites de ConfigHardware.h
        self.TEMP_MINIMA = 2.0
        self.TEMP_MAXIMA = 8.0

        self.comunicacion = ComunicacionSerial(
            al_recibir_lectura=self._on_lectura_thread_safe,
            al_recibir_evento=self._on_evento_thread_safe
        )

        self._crear_widgets()

    def _crear_widgets(self):
        # Panel de Conexión
        panel_conn = tk.LabelFrame(self.root, text=" Enlace Serial UART (115200 bps) ", bg="#242436", fg="white", font=("Arial", 10, "bold"))
        panel_conn.pack(fill="x", padx=15, pady=10)

        tk.Label(panel_conn, text="Puerto:", bg="#242436", fg="white").pack(side="left", padx=10, pady=8)
        self.combo_puertos = ttk.Combobox(panel_conn, values=self.comunicacion.obtener_puertos(), width=18)
        self.combo_puertos.pack(side="left", padx=5)
        if self.combo_puertos["values"]:
            self.combo_puertos.current(0)

        tk.Button(panel_conn, text="Actualizar", command=self._actualizar_puertos, bg="#3a3a54", fg="white").pack(side="left", padx=5)
        self.btn_conectar = tk.Button(panel_conn, text="Conectar", command=self._alternar_conexion, bg="#28a745", fg="white", font=("Arial", 9, "bold"), width=12)
        self.btn_conectar.pack(side="left", padx=10)

        self.lbl_estado = tk.Label(panel_conn, text="● DESCONECTADO", bg="#242436", fg="#ff5555", font=("Arial", 10, "bold"))
        self.lbl_estado.pack(side="right", padx=15)

        # Panel de Monitoreo en Tiempo Real
        panel_sensores = tk.LabelFrame(self.root, text=" Monitoreo de Sensores DS18B20 ", bg="#242436", fg="white", font=("Arial", 10, "bold"))
        panel_sensores.pack(fill="x", padx=15, pady=5)

        # Temperatura Interna
        card_int = tk.Frame(panel_sensores, bg="#181824", bd=2, relief="groove")
        card_int.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        tk.Label(card_int, text="TEMP. INTERNA (Cámara)", bg="#181824", fg="#a0a0c0", font=("Arial", 9, "bold")).pack(pady=(8, 0))
        self.lbl_t_int = tk.Label(card_int, text="--.- °C", bg="#181824", fg="#00ffcc", font=("Arial", 26, "bold"))
        self.lbl_t_int.pack(pady=5)
        self.barra_t_int = ttk.Progressbar(card_int, length=180, mode="determinate", maximum=40)
        self.barra_t_int.pack(pady=(0, 10))

        # Temperatura Externa
        card_ext = tk.Frame(panel_sensores, bg="#181824", bd=2, relief="groove")
        card_ext.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        tk.Label(card_ext, text="TEMP. EXTERNA (Ambiente)", bg="#181824", fg="#a0a0c0", font=("Arial", 9, "bold")).pack(pady=(8, 0))
        self.lbl_t_ext = tk.Label(card_ext, text="--.- °C", bg="#181824", fg="#66b3ff", font=("Arial", 26, "bold"))
        self.lbl_t_ext.pack(pady=5)
        self.barra_t_ext = ttk.Progressbar(card_ext, length=180, mode="determinate", maximum=50)
        self.barra_t_ext.pack(pady=(0, 10))

        # Indicador de Alarma
        self.lbl_semaforo = tk.Label(panel_sensores, text="ESPERANDO\nLECTURAS", bg="#444466", fg="white", font=("Arial", 11, "bold"), width=22)
        self.lbl_semaforo.pack(side="right", fill="y", padx=10, pady=10)

        # Panel de Control Remoto
        panel_control = tk.LabelFrame(self.root, text=" Control Remoto de Actuadores ", bg="#242436", fg="white", font=("Arial", 10, "bold"))
        panel_control.pack(fill="x", padx=15, pady=5)

        tk.Button(panel_control, text="Forzar Alarma (ON)", bg="#dc3545", fg="white", font=("Arial", 9, "bold"),
                  command=lambda: self.comunicacion.enviar("ALARMA_ON")).pack(side="left", padx=12, pady=12)

        tk.Button(panel_control, text="Normalizar Alarma (OFF)", bg="#17a2b8", fg="white", font=("Arial", 9, "bold"),
                  command=lambda: self.comunicacion.enviar("ALARMA_OFF")).pack(side="left", padx=5, pady=12)

        tk.Label(panel_control, text="Potencia PWM (0-255):", bg="#242436", fg="white").pack(side="left", padx=(20, 5))
        self.slider_pwm = tk.Scale(panel_control, from_=0, to=255, orient="horizontal", bg="#242436", fg="white", highlightthickness=0, length=150)
        self.slider_pwm.pack(side="left", padx=5)

        tk.Button(panel_control, text="Enviar PWM", bg="#ffc107", fg="black", font=("Arial", 9, "bold"),
                  command=self._enviar_pwm).pack(side="left", padx=10)

        # Bitácora de Eventos
        panel_log = tk.LabelFrame(self.root, text=" Registro de Eventos y Alarmas (Bitácora) ", bg="#242436", fg="white", font=("Arial", 10, "bold"))
        panel_log.pack(fill="both", expand=True, padx=15, pady=(5, 15))

        self.txt_log = scrolledtext.ScrolledText(panel_log, height=8, bg="#101018", fg="#00ff66", font=("Consolas", 9), state="disabled")
        self.txt_log.pack(fill="both", expand=True, padx=10, pady=10)

    def _actualizar_puertos(self):
        self.combo_puertos["values"] = self.comunicacion.obtener_puertos()

    def _alternar_conexion(self):
        if not self.comunicacion.conectado:
            puerto = self.combo_puertos.get()
            if not puerto:
                messagebox.showwarning("Puerto requerido", "Selecciona un puerto COM disponible.")
                return
            if self.comunicacion.conectar(puerto):
                self.btn_conectar.config(text="Desconectar", bg="#dc3545")
                self.lbl_estado.config(text=f"● CONECTADO ({puerto})", fg="#00ff88")
                self._agregar_log(f"Conectado al ESP32 en {puerto}.")
        else:
            self.comunicacion.desconectar()
            self.btn_conectar.config(text="Conectar", bg="#28a745")
            self.lbl_estado.config(text="● DESCONECTADO", fg="#ff5555")
            self._agregar_log("Conexión serial cerrada.")

    def _enviar_pwm(self):
        self.comunicacion.enviar(f"PWM:{self.slider_pwm.get()}")

    # Callbacks Thread-Safe para Tkinter
    def _on_lectura_thread_safe(self, t_int, t_ext):
        self.root.after(0, self._actualizar_dashboard, t_int, t_ext)

    def _on_evento_thread_safe(self, texto):
        self.root.after(0, self._agregar_log, texto)

    def _actualizar_dashboard(self, t_int, t_ext):
        self.lbl_t_int.config(text=f"{t_int:.2f} °C")
        self.lbl_t_ext.config(text=f"{t_ext:.2f} °C")

        self.barra_t_int["value"] = max(0, min(40, t_int))
        self.barra_t_ext["value"] = max(0, min(50, t_ext))

        if t_int < self.TEMP_MINIMA or t_int > self.TEMP_MAXIMA:
            self.lbl_t_int.config(fg="#ff4444")
            self.lbl_semaforo.config(text="¡ALERTA TÉRMICA!\nFUERA DE RANGO", bg="#cc0000")
            self._agregar_log(f"[ALARMA] Temp. Interna: {t_int:.2f} °C fuera de [{self.TEMP_MINIMA}, {self.TEMP_MAXIMA}] °C")
        else:
            self.lbl_t_int.config(fg="#00ffcc")
            self.lbl_semaforo.config(text="OPERACIÓN NORMAL\nRANGO ÓPTIMO", bg="#28a745")
            self._agregar_log(f"[OK] Interna: {t_int:.2f} °C | Externa: {t_ext:.2f} °C")

    def _agregar_log(self, mensaje):
        marca_tiempo = datetime.now().strftime("%H:%M:%S")
        self.txt_log.configure(state="normal")
        self.txt_log.insert(tk.END, f"[{marca_tiempo}] {mensaje}\n")
        self.txt_log.see(tk.END)
        self.txt_log.configure(state="disabled")

    def cerrar_aplicacion(self):
        self.comunicacion.desconectar()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardHMI(root)
    root.protocol("WM_DELETE_WINDOW", app.cerrar_aplicacion)
    root.mainloop()
