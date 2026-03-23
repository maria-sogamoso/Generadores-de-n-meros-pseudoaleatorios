import tkinter as tk
from tkinter import filedialog, messagebox

import ttkbootstrap as ttk

from app_services import (
    ExportacionService,
    GeneracionService,
    GraficosService,
    SemillasService,
    ValidacionService,
)
class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("Generador de Numeros Pseudoaleatorios - Interfaz")
        self.geometry("1800x800")

        self.semillas_archivo = []
        self.secuencias = {}  # clave corrida -> lista Ri
        self.corridas_info = {}  # clave corrida -> (metodo, semilla, seq)
        self.corridas_var = tk.IntVar(value=30)

        self.semillas_service = SemillasService()
        self.generacion_service = GeneracionService()
        self.validacion_service = ValidacionService()
        self.graficos_service = GraficosService()
        self.exportacion_service = ExportacionService()

        self._build_ui()

    def _build_ui(self):
        # Contenedor principal con 3 secciones: config, acciones, y tablas
        main_container = ttk.Frame(self, padding=10)
        main_container.pack(fill="both", expand=True)

        # ============ SECCIÓN DE CONFIGURACIÓN (2 COLUMNAS) ============
        config_frame = ttk.Frame(main_container)
        config_frame.pack(fill="x", pady=(0, 10))

        # Columna izquierda: Semillas y Métodos
        left_column = ttk.Frame(config_frame)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Entrada de semillas
        semillas_frame = ttk.Labelframe(left_column, text="Entrada de semillas", padding=10, bootstyle="success")
        semillas_frame.pack(fill="x", pady=(0, 5))

        self.modo_semilla = tk.StringVar(value="manual")
        ttk.Radiobutton(
            semillas_frame, text="Manual", variable=self.modo_semilla, value="manual"
        ).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(
            semillas_frame, text="Archivo (.txt/.csv)", variable=self.modo_semilla, value="archivo"
        ).grid(row=0, column=1, sticky="w")

        ttk.Label(semillas_frame, text="Semillas manuales (ej: 123, 456, 789):").grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(6, 0)
        )
        self.entry_semillas = ttk.Entry(semillas_frame, width=40)
        self.entry_semillas.grid(row=2, column=0, columnspan=2, sticky="we", pady=2)

        ttk.Button(
            semillas_frame, text="Cargar archivo", command=self._cargar_archivo_semillas, bootstyle="secondary"
        ).grid(row=2, column=2, padx=8)
        self.lbl_archivo = ttk.Label(semillas_frame, text="Sin archivo cargado")
        self.lbl_archivo.grid(row=1, column=2, sticky="w")

        # Seleccion de metodos
        metodos_container = ttk.Frame(left_column)
        metodos_container.pack(fill="x", pady=5)

        metodos_frame = ttk.Labelframe(
            metodos_container,
            text="Metodos de generacion base",
            padding=10,
            bootstyle="success",
        )
        metodos_frame.pack(side="left", fill="x", expand=True)

        dist_frame = ttk.Labelframe(
            metodos_container,
            text="Metodos por distribucion",
            padding=10,
            bootstyle="warning",
        )
        dist_frame.pack(side="left", fill="x", expand=True, padx=(8, 0))

        self.metodos_vars = {
            "Cuadrados Medios": tk.BooleanVar(value=True),
            "Congruencia Lineal": tk.BooleanVar(value=True),
            "Congruencial Multiplicativo": tk.BooleanVar(value=False),
            "Congruencial Aditivo": tk.BooleanVar(value=False),
        }
        col = 0
        for nombre, var in self.metodos_vars.items():
            ttk.Checkbutton(
                metodos_frame,
                text=nombre,
                variable=var,
                command=self._actualizar_parametros_metodos,
            ).grid(row=col, column=0, sticky="w", padx=6, pady=3)
            col += 1

        self.metodos_distribucion_vars = {
            "Distribucion Uniforme": tk.BooleanVar(value=False),
            "Distribucion Normal": tk.BooleanVar(value=False),
        }
        self.chk_distribuciones = []

        row = 0
        for nombre, var in self.metodos_distribucion_vars.items():
            chk = ttk.Checkbutton(
                dist_frame,
                text=nombre,
                variable=var,
                command=self._actualizar_estado_distribuciones,
            )
            chk.grid(row=row, column=0, sticky="w", padx=6, pady=3)
            self.chk_distribuciones.append(chk)
            row += 1

        # Columna derecha: Parámetros y Pruebas
        right_column = ttk.Frame(config_frame)
        right_column.pack(side="right", fill="both", expand=True, padx=(5, 0))

        # Parametros globales
        params_frame = ttk.Labelframe(right_column, text="Parametros", padding=10, bootstyle="info")
        params_frame.pack(fill="x", pady=(0, 5))

        ttk.Label(params_frame, text="Pasos:").grid(row=0, column=0, sticky="w")
        self.pasos_var = tk.IntVar(value=1000)
        ttk.Entry(params_frame, textvariable=self.pasos_var, width=12).grid(row=0, column=1, sticky="w")

        self.lbl_digitos = ttk.Label(params_frame, text="Digitos:")
        self.lbl_digitos.grid(row=1, column=0, sticky="w", pady=5)
        self.digitos_var = tk.IntVar(value=8)
        self.entry_digitos = ttk.Entry(params_frame, textvariable=self.digitos_var, width=12)
        self.entry_digitos.grid(row=1, column=1, sticky="w")

        self.lbl_a_mult = ttk.Label(params_frame, text="a multip.:")
        self.lbl_a_mult.grid(row=2, column=0, sticky="w", pady=5)
        self.a_mult_var = tk.IntVar(value=1664525)
        self.entry_a_mult = ttk.Entry(params_frame, textvariable=self.a_mult_var, width=12)
        self.entry_a_mult.grid(row=2, column=1, sticky="w")

        self.lbl_m = ttk.Label(params_frame, text="m:")
        self.lbl_m.grid(row=3, column=0, sticky="w", pady=5)
        self.m_var = tk.IntVar(value=2**32)
        self.entry_m = ttk.Entry(params_frame, textvariable=self.m_var, width=14)
        self.entry_m.grid(row=3, column=1, sticky="w")

        self.lbl_corridas = ttk.Label(params_frame, text="Corridas:")
        self.lbl_corridas.grid(row=4, column=0, sticky="w", pady=5)
        self.entry_corridas = ttk.Entry(
            params_frame,
            textvariable=self.corridas_var,
            width=10,
        )
        self.entry_corridas.grid(row=4, column=1, sticky="w")

        self.lbl_u_a = ttk.Label(params_frame, text="Uniforme a:")
        self.lbl_u_a.grid(row=5, column=0, sticky="w", pady=5)
        self.uniforme_a_var = tk.DoubleVar(value=0.0)
        self.entry_u_a = ttk.Entry(params_frame, textvariable=self.uniforme_a_var, width=12)
        self.entry_u_a.grid(row=5, column=1, sticky="w")

        self.lbl_u_b = ttk.Label(params_frame, text="Uniforme b:")
        self.lbl_u_b.grid(row=6, column=0, sticky="w", pady=5)
        self.uniforme_b_var = tk.DoubleVar(value=1.0)
        self.entry_u_b = ttk.Entry(params_frame, textvariable=self.uniforme_b_var, width=12)
        self.entry_u_b.grid(row=6, column=1, sticky="w")

        self.lbl_n_mu = ttk.Label(params_frame, text="Normal mu:")
        self.lbl_n_mu.grid(row=7, column=0, sticky="w", pady=5)
        self.normal_mu_var = tk.DoubleVar(value=0.0)
        self.entry_n_mu = ttk.Entry(params_frame, textvariable=self.normal_mu_var, width=12)
        self.entry_n_mu.grid(row=7, column=1, sticky="w")

        self.lbl_n_sigma = ttk.Label(params_frame, text="Normal sigma:")
        self.lbl_n_sigma.grid(row=8, column=0, sticky="w", pady=5)
        self.normal_sigma_var = tk.DoubleVar(value=1.0)
        self.entry_n_sigma = ttk.Entry(params_frame, textvariable=self.normal_sigma_var, width=12)
        self.entry_n_sigma.grid(row=8, column=1, sticky="w")


        # Seleccion de pruebas
        pruebas_frame = ttk.Labelframe(right_column, text="Pruebas de validacion", padding=10, bootstyle="info")
        pruebas_frame.pack(fill="x", pady=5)

        self.pruebas_vars = {
            "Chi Cuadrado": tk.BooleanVar(value=True),
            "Kolmogorov Smirnov": tk.BooleanVar(value=True),
            "Medias": tk.BooleanVar(value=True),
            "Varianza": tk.BooleanVar(value=True),
            "Poker": tk.BooleanVar(value=False),
            "Rachas": tk.BooleanVar(value=False),
        }
        col = 0
        row = 0
        for nombre, var in self.pruebas_vars.items():
            ttk.Checkbutton(
                pruebas_frame,
                text=nombre,
                variable=var,
                command=self._actualizar_estado_corridas,
            ).grid(row=row, column=col, sticky="w", padx=6, pady=3)
            row += 1
            if row == 3:
                row = 0
                col = 1
        self._actualizar_estado_corridas()
        self._actualizar_parametros_metodos()
        self._actualizar_estado_distribuciones()

        # ============ SECCIÓN DE ACCIONES Y GRÁFICOS ============
        acciones = ttk.Frame(main_container)
        acciones.pack(fill="x", pady=8)
        ttk.Button(acciones, text="Ejecutar", command=self._ejecutar, bootstyle="success").pack(side="left")
        ttk.Button(acciones, text="Exportar secuencias", command=self._exportar_secuencias, bootstyle="primary-outline").pack(side="left", padx=8)
        ttk.Button(acciones, text="Exportar validaciones", command=self._exportar_validaciones, bootstyle="primary-outline").pack(side="left", padx=8)

        ttk.Label(acciones, text="Corrida para graficar:").pack(side="left", padx=(20, 4))
        self.combo_corrida = ttk.Combobox(acciones, state="readonly", width=40)
        self.combo_corrida.pack(side="left")

        ttk.Label(acciones, text="Grafico:").pack(side="left", padx=(12, 4))
        self.combo_grafico = ttk.Combobox(
            acciones,
            state="readonly",
            values=[
                "Histograma",
                "Chi Cuadrado",
                "Kolmogorov Smirnov",
                "Medias",
                "Varianza",
                "Poker",
                "Rachas",
            ],
            width=22,
        )
        self.combo_grafico.set("Histograma")
        self.combo_grafico.pack(side="left")
        ttk.Button(acciones, text="Mostrar grafico", command=self._mostrar_grafico, bootstyle="info").pack(side="left", padx=8)

        # ============ SECCIÓN DE TABLAS ============
        tablas = ttk.Panedwindow(main_container, orient=tk.VERTICAL)
        tablas.pack(fill="both", expand=True, pady=(10, 0))

        frame_seq = ttk.Labelframe(tablas, text="Secuencias generadas (exportables)", padding=8, bootstyle="secondary")
        frame_val = ttk.Labelframe(tablas, text="Resultados de validacion", padding=8, bootstyle="secondary")
        tablas.add(frame_seq, weight=3)
        tablas.add(frame_val, weight=2)

        self.tabla_seq = ttk.Treeview(
            frame_seq,
            columns=("corrida", "metodo", "semilla", "indice", "ri"),
            show="headings",
            height=14,
        )
        for c, w in [("corrida", 280), ("metodo", 210), ("semilla", 120), ("indice", 90), ("ri", 160)]:
            self.tabla_seq.heading(c, text=c)
            self.tabla_seq.column(c, width=w, anchor="center")
        self.tabla_seq.pack(fill="both", expand=True)

        self.tabla_val = ttk.Treeview(
            frame_val,
            columns=("corrida", "prueba", "resultado", "detalle"),
            show="headings",
            height=8,
        )
        for c, w in [("corrida", 300), ("prueba", 200), ("resultado", 110), ("detalle", 520)]:
            self.tabla_val.heading(c, text=c)
            self.tabla_val.column(c, width=w, anchor="center")
        self.tabla_val.pack(fill="both", expand=True)

    def _parse_semillas_texto(self, texto):
        return self.semillas_service.parsear_texto(texto)

    def _leer_semillas_archivo(self, path):
        return self.semillas_service.leer_archivo(path)

    def _cargar_archivo_semillas(self):
        path = filedialog.askopenfilename(
            title="Seleccionar archivo de semillas",
            filetypes=[("Archivos de texto", "*.txt *.csv"), ("Todos", "*.*")],
        )
        if not path:
            return
        try:
            semillas = self._leer_semillas_archivo(path)
            if not semillas:
                raise ValueError("El archivo no contiene semillas validas.")
            self.semillas_archivo = semillas
            self.lbl_archivo.config(text=f"Archivo cargado: {path}")
            messagebox.showinfo("Semillas", f"Se cargaron {len(semillas)} semillas.")
        except Exception as e:
            messagebox.showerror("Error al cargar archivo", str(e))

    def _obtener_semillas(self):
        if self.modo_semilla.get() == "archivo":
            if not self.semillas_archivo:
                raise ValueError("Debes cargar un archivo con semillas.")
            return self.semillas_archivo
        texto = self.entry_semillas.get().strip()
        if not texto:
            raise ValueError("Ingresa semillas manuales.")
        semillas = self._parse_semillas_texto(texto)
        if not semillas:
            raise ValueError("No se detectaron semillas validas.")
        return semillas

    def _actualizar_estado_corridas(self):
        requiere_corridas = (
            self.pruebas_vars["Medias"].get()
            or self.pruebas_vars["Varianza"].get()
        )
        self._set_visibilidad_parametro(self.lbl_corridas, self.entry_corridas, requiere_corridas)

    def _actualizar_estado_distribuciones(self):
        hay_base = any(var.get() for var in self.metodos_vars.values())
        usa_uniforme = self.metodos_distribucion_vars["Distribucion Uniforme"].get()
        usa_normal = self.metodos_distribucion_vars["Distribucion Normal"].get()

        if not hay_base:
            for var in self.metodos_distribucion_vars.values():
                var.set(False)
            usa_uniforme = False
            usa_normal = False

        for chk in self.chk_distribuciones:
            if hay_base:
                chk.configure(state="normal")
            else:
                chk.configure(state="disabled")

        self._set_visibilidad_parametro(self.lbl_u_a, self.entry_u_a, usa_uniforme)
        self._set_visibilidad_parametro(self.lbl_u_b, self.entry_u_b, usa_uniforme)
        self._set_visibilidad_parametro(self.lbl_n_mu, self.entry_n_mu, usa_normal)
        self._set_visibilidad_parametro(self.lbl_n_sigma, self.entry_n_sigma, usa_normal)

    def _actualizar_parametros_metodos(self):
        usa_cuadrados = self.metodos_vars["Cuadrados Medios"].get()
        usa_multiplicativo = self.metodos_vars["Congruencial Multiplicativo"].get()
        usa_aditivo = self.metodos_vars["Congruencial Aditivo"].get()
        usa_m = usa_multiplicativo or usa_aditivo

        self._set_visibilidad_parametro(self.lbl_digitos, self.entry_digitos, usa_cuadrados)
        self._set_visibilidad_parametro(self.lbl_a_mult, self.entry_a_mult, usa_multiplicativo)
        self._set_visibilidad_parametro(self.lbl_m, self.entry_m, usa_m)
        self._actualizar_estado_distribuciones()

    @staticmethod
    def _set_visibilidad_parametro(label_widget, entry_widget, visible):
        if visible:
            label_widget.grid()
            entry_widget.grid()
        else:
            label_widget.grid_remove()
            entry_widget.grid_remove()

    def _generar_por_metodo(self, metodo, semillas, pasos, corridas=1):
        return self.generacion_service.generar_por_metodo(
            metodo=metodo,
            semillas=semillas,
            pasos=pasos,
            corridas=corridas,
            digitos=self.digitos_var.get(),
            a_mult=self.a_mult_var.get(),
            m=self.m_var.get(),
        )

    def _ejecutar_pruebas(self, seq, metodo):
        pruebas = [p for p, v in self.pruebas_vars.items() if v.get()]
        params_dist = {
            "a": self.uniforme_a_var.get(),
            "b": self.uniforme_b_var.get(),
            "mu": self.normal_mu_var.get(),
            "sigma": self.normal_sigma_var.get(),
        }
        return self.validacion_service.ejecutar_pruebas(
            seq,
            pruebas,
            metodo=metodo,
            params_dist=params_dist,
        )

    def _ejecutar(self):
        try:
            pasos = self.pasos_var.get()
            if pasos <= 0:
                raise ValueError("Pasos debe ser mayor a 0.")

            semillas = self._obtener_semillas()
            metodos = [m for m, v in self.metodos_vars.items() if v.get()]
            metodos_distribucion = [
                m for m, v in self.metodos_distribucion_vars.items() if v.get()
            ]

            if not metodos and not metodos_distribucion:
                raise ValueError("Selecciona al menos un metodo.")
            if metodos_distribucion and not metodos:
                raise ValueError(
                    "Para usar distribuciones debes seleccionar al menos un generador base."
                )

            requiere_corridas = (
                self.pruebas_vars["Medias"].get()
                or self.pruebas_vars["Varianza"].get()
            )
            total_corridas = self.corridas_var.get() if requiere_corridas else 1
            if total_corridas <= 0:
                raise ValueError("Corridas debe ser mayor a 0.")
            if requiere_corridas and total_corridas < 2:
                raise ValueError(
                    "Para Medias/Varianza debes usar al menos 2 corridas."
                )

            # limpiar tablas y estado
            for i in self.tabla_seq.get_children():
                self.tabla_seq.delete(i)
            for i in self.tabla_val.get_children():
                self.tabla_val.delete(i)
            self.secuencias.clear()
            self.corridas_info.clear()

            corridas_totales = {}

            for metodo in metodos:
                corridas = self._generar_por_metodo(
                    metodo,
                    semillas,
                    pasos,
                    corridas=total_corridas,
                )
                corridas_totales.update(corridas)

            if metodos_distribucion:
                corridas_dist = self.generacion_service.generar_distribuciones_desde_bases(
                    corridas_base=corridas_totales,
                    incluir_uniforme="Distribucion Uniforme" in metodos_distribucion,
                    incluir_normal="Distribucion Normal" in metodos_distribucion,
                    a=self.uniforme_a_var.get(),
                    b=self.uniforme_b_var.get(),
                    mu=self.normal_mu_var.get(),
                    sigma=self.normal_sigma_var.get(),
                )
                corridas_totales.update(corridas_dist)

            for corrida, (met, sem, seq) in corridas_totales.items():
                self.secuencias[corrida] = seq
                self.corridas_info[corrida] = (met, sem, seq)

                for i, ri in enumerate(seq, start=1):
                    self.tabla_seq.insert("", "end", values=(corrida, met, sem, i, f"{ri:.10f}"))

                res = self._ejecutar_pruebas(seq, met)
                for prueba, ok, detalle in res:
                    self.tabla_val.insert(
                        "", "end",
                        values=(corrida, prueba, "Aceptada" if ok else "Rechazada", detalle)
                    )

            self.combo_corrida["values"] = list(self.secuencias.keys())
            if self.secuencias:
                self.combo_corrida.current(0)

            messagebox.showinfo("Proceso finalizado", "Generacion, validacion y tablas listas.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _mostrar_grafico(self):
        corrida = self.combo_corrida.get()
        if not corrida:
            messagebox.showwarning("Grafico", "Selecciona una corrida.")
            return

        seq = self.secuencias.get(corrida, [])
        if not seq:
            messagebox.showwarning("Grafico", "No hay datos para graficar.")
            return

        tipo = self.combo_grafico.get()

        if tipo != "Histograma":
            var_prueba = self.pruebas_vars.get(tipo)
            if var_prueba is None or not var_prueba.get():
                messagebox.showwarning(
                    "Grafico",
                    f"La prueba '{tipo}' no fue seleccionada. Actívala y ejecuta nuevamente.",
                )
                return

        metodo = self.corridas_info.get(corrida, (None, None, None))[0]
        params_dist = {
            "a": self.uniforme_a_var.get(),
            "b": self.uniforme_b_var.get(),
            "mu": self.normal_mu_var.get(),
            "sigma": self.normal_sigma_var.get(),
        }

        try:
            self.graficos_service.mostrar(
                tipo=tipo,
                corrida=corrida,
                seq=seq,
                secuencias=self.secuencias,
                metodo=metodo,
                params_dist=params_dist,
                corridas_info=self.corridas_info,
            )
        except Exception as e:
            messagebox.showerror("Error al graficar", str(e))

    def _exportar_treeview_csv(self, treeview, columnas, sugerido):
        self.exportacion_service.exportar_treeview_csv(treeview, columnas, sugerido)

    def _exportar_secuencias(self):
        self._exportar_treeview_csv(
            self.tabla_seq,
            ["corrida", "metodo", "semilla", "indice", "ri"],
            "secuencias_generadas.csv",
        )

    def _exportar_validaciones(self):
        self._exportar_treeview_csv(
            self.tabla_val,
            ["corrida", "prueba", "resultado", "detalle"],
            "resultados_validacion.csv",
        )

if __name__ == "__main__":
    app = App()
    app.mainloop()
