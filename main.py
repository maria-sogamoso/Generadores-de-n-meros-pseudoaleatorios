import csv
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2, norm 

from generador_numeros.cuadrados_medios import GeneradorCuadradosMedios
from generador_numeros.congruencia_lineal import GeneradorCongruenciaLineal
from generador_numeros.congruencial_multiplicativo import GeneradorCongruencialMultiplicativo
from generador_numeros.congruencial_aditivo import GeneradorCongruencialAditivo

from validadores.prueba_chi_cuadrado import PruebaChiCuadrado
from validadores.prueba_kolmogorov_smirnov import PruebaKolmogorovSmirnov
from validadores.prueba_medias import PruebaMedias
from validadores.prueba_varianza import PruebaVarianza
from validadores.prueba_poker import PruebaPoker
from validadores.prueba_rachas import PruebaRachas

from visualizaciones.graficas_de_validacion import (
    graficar_kolmogorov_smirnov,
    graficar_prueba_chi_cuadrado,
    graficar_prueba_poker,
    graficar_prueba_rachas,
    graficar_prueba_medias,
    graficar_prueba_varianza,
)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Generador de Numeros Pseudoaleatorios - Interfaz")
        self.geometry("1300x760")

        self.semillas_archivo = []
        self.secuencias = {}  # clave corrida -> lista Ri
        self.corridas_var = tk.IntVar(value=30)

        self._build_ui()

    def _build_ui(self):
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        # Entrada de semillas
        semillas_frame = ttk.LabelFrame(top, text="Entrada de semillas", padding=10)
        semillas_frame.pack(fill="x", pady=5)

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
        self.entry_semillas = ttk.Entry(semillas_frame, width=80)
        self.entry_semillas.grid(row=2, column=0, columnspan=2, sticky="we", pady=2)

        ttk.Button(
            semillas_frame, text="Cargar archivo", command=self._cargar_archivo_semillas
        ).grid(row=2, column=2, padx=8)
        self.lbl_archivo = ttk.Label(semillas_frame, text="Sin archivo cargado")
        self.lbl_archivo.grid(row=1, column=2, sticky="w")

        # Parametros globales
        params_frame = ttk.LabelFrame(top, text="Parametros", padding=10)
        params_frame.pack(fill="x", pady=5)

        ttk.Label(params_frame, text="Cantidad de numeros (pasos):").grid(row=0, column=0, sticky="w")
        self.pasos_var = tk.IntVar(value=1000)
        ttk.Entry(params_frame, textvariable=self.pasos_var, width=12).grid(row=0, column=1, sticky="w")

        ttk.Label(params_frame, text="Digitos cuadrados medios:").grid(row=0, column=2, sticky="w", padx=(20, 0))
        self.digitos_var = tk.IntVar(value=8)
        ttk.Entry(params_frame, textvariable=self.digitos_var, width=10).grid(row=0, column=3, sticky="w")

        ttk.Label(params_frame, text="a multiplicativo:").grid(row=0, column=4, sticky="w", padx=(20, 0))
        self.a_mult_var = tk.IntVar(value=1664525)
        ttk.Entry(params_frame, textvariable=self.a_mult_var, width=12).grid(row=0, column=5, sticky="w")

        ttk.Label(params_frame, text="m multiplicativo/aditivo:").grid(row=0, column=6, sticky="w", padx=(20, 0))
        self.m_var = tk.IntVar(value=2**32)
        ttk.Entry(params_frame, textvariable=self.m_var, width=14).grid(row=0, column=7, sticky="w")

        ttk.Label(params_frame, text="Corridas (solo Medias/Varianza):").grid(
            row=0, column=8, sticky="w", padx=(20, 0)
        )
        self.entry_corridas = ttk.Entry(
            params_frame,
            textvariable=self.corridas_var,
            width=10,
            state="disabled",
        )
        self.entry_corridas.grid(row=0, column=9, sticky="w")

        # Seleccion de metodos
        metodos_frame = ttk.LabelFrame(top, text="Metodos de generacion", padding=10)
        metodos_frame.pack(fill="x", pady=5)

        self.metodos_vars = {
            "Cuadrados Medios": tk.BooleanVar(value=True),
            "Congruencia Lineal": tk.BooleanVar(value=True),
            "Congruencial Multiplicativo": tk.BooleanVar(value=False),
            "Congruencial Aditivo": tk.BooleanVar(value=False),
        }
        col = 0
        for nombre, var in self.metodos_vars.items():
            ttk.Checkbutton(metodos_frame, text=nombre, variable=var).grid(row=0, column=col, sticky="w", padx=6)
            col += 1

        # Seleccion de pruebas
        pruebas_frame = ttk.LabelFrame(top, text="Pruebas de validacion", padding=10)
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
        for nombre, var in self.pruebas_vars.items():
            ttk.Checkbutton(
                pruebas_frame,
                text=nombre,
                variable=var,
                command=self._actualizar_estado_corridas,
            ).grid(row=0, column=col, sticky="w", padx=6)
            col += 1
        self._actualizar_estado_corridas()

        acciones = ttk.Frame(top)
        acciones.pack(fill="x", pady=8)
        ttk.Button(acciones, text="Ejecutar", command=self._ejecutar).pack(side="left")
        ttk.Button(acciones, text="Exportar secuencias", command=self._exportar_secuencias).pack(side="left", padx=8)
        ttk.Button(acciones, text="Exportar validaciones", command=self._exportar_validaciones).pack(side="left", padx=8)

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
        ttk.Button(acciones, text="Mostrar grafico", command=self._mostrar_grafico).pack(side="left", padx=8)

        # Tablas
        tablas = ttk.Panedwindow(self, orient=tk.VERTICAL)
        tablas.pack(fill="both", expand=True, padx=10, pady=10)

        frame_seq = ttk.LabelFrame(tablas, text="Secuencias generadas (exportables)", padding=8)
        frame_val = ttk.LabelFrame(tablas, text="Resultados de validacion", padding=8)
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
        tokens = re.split(r"[,\s;]+", texto.strip())
        semillas = []
        for t in tokens:
            if t == "":
                continue
            semillas.append(int(t))
        return semillas

    def _leer_semillas_archivo(self, path):
        with open(path, "r", encoding="utf-8") as f:
            contenido = f.read()
        return self._parse_semillas_texto(contenido)

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
        self.entry_corridas.config(state="normal" if requiere_corridas else "disabled")

    def _generar_por_metodo(self, metodo, semillas, pasos, corridas=1):
        corridas_generadas = {}
        if metodo == "Cuadrados Medios":
            d = self.digitos_var.get()
            for s in semillas:
                for i in range(corridas):
                    semilla_i = s + i
                    gen = GeneradorCuadradosMedios(semilla=semilla_i, digitos=d)
                    seq = gen.siguiente_Ri_Cuadrados_Medios(pasos)
                    key = f"{metodo} | corrida={i + 1} | semilla={semilla_i}"
                    corridas_generadas[key] = (metodo, semilla_i, seq)

        elif metodo == "Congruencia Lineal":
            for s in semillas:
                for i in range(corridas):
                    semilla_i = s + i
                    gen = GeneradorCongruenciaLineal(semilla=semilla_i)
                    seq = gen.siguiente_Ri_Congruencia_Lineal(pasos)
                    key = f"{metodo} | corrida={i + 1} | semilla={semilla_i}"
                    corridas_generadas[key] = (metodo, semilla_i, seq)

        elif metodo == "Congruencial Multiplicativo":
            a = self.a_mult_var.get()
            m = self.m_var.get()
            for s in semillas:
                for i in range(corridas):
                    semilla_i = s + i
                    gen = GeneradorCongruencialMultiplicativo(
                        semilla=semilla_i,
                        a=a,
                        m=m,
                    )
                    seq = gen.siguiente_Ri_Congruencial_Multiplicativo(pasos)
                    key = f"{metodo} | corrida={i + 1} | semilla={semilla_i}"
                    corridas_generadas[key] = (metodo, semilla_i, seq)

        elif metodo == "Congruencial Aditivo":
            if len(semillas) < 2:
                raise ValueError("Congruencial aditivo requiere al menos 2 semillas.")
            m = self.m_var.get()
            for i in range(corridas):
                semillas_i = [s + i for s in semillas]
                gen = GeneradorCongruencialAditivo(semillas_iniciales=semillas_i, m=m)
                seq = gen.siguiente_Ri_Congruencial_Aditivo(pasos)
                key = f"{metodo} | corrida={i + 1} | semillas={semillas_i}"
                corridas_generadas[key] = (metodo, f"lista+{i}", seq)

        return corridas_generadas

    def _ejecutar_pruebas(self, seq):
        resultados = []
        pruebas = [p for p, v in self.pruebas_vars.items() if v.get()]

        for p in pruebas:
            try:
                if p == "Chi Cuadrado":
                    k = max(10, min(100, len(seq) // 5))
                    ok = PruebaChiCuadrado().prueba_chi_cuadrado(seq, k=k)
                    resultados.append((p, ok, f"k={k}"))
                elif p == "Kolmogorov Smirnov":
                    ok = PruebaKolmogorovSmirnov().prueba_kolmogorov_smirnov(seq)
                    resultados.append((p, ok, "alpha=0.05"))
                elif p == "Medias":
                    ok = PruebaMedias().prueba_medias(seq)
                    resultados.append((p, ok, "alpha=0.05"))
                elif p == "Varianza":
                    ok = PruebaVarianza().prueba_varianza(seq)
                    resultados.append((p, ok, "alpha=0.05"))
                elif p == "Poker":
                    ok = PruebaPoker().prueba_poker(seq)
                    resultados.append((p, ok, "5 digitos"))
                elif p == "Rachas":
                    ok = PruebaRachas().prueba_rachas(seq)
                    resultados.append((p, ok, "mediana=0.5"))
            except Exception as e:
                resultados.append((p, False, f"Error: {e}"))

        return resultados

    def _ejecutar(self):
        try:
            pasos = self.pasos_var.get()
            if pasos <= 0:
                raise ValueError("Pasos debe ser mayor a 0.")

            semillas = self._obtener_semillas()
            metodos = [m for m, v in self.metodos_vars.items() if v.get()]
            if not metodos:
                raise ValueError("Selecciona al menos un metodo.")

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

            for metodo in metodos:
                corridas = self._generar_por_metodo(
                    metodo,
                    semillas,
                    pasos,
                    corridas=total_corridas,
                )
                for corrida, (met, sem, seq) in corridas.items():
                    self.secuencias[corrida] = seq

                    for i, ri in enumerate(seq, start=1):
                        self.tabla_seq.insert("", "end", values=(corrida, met, sem, i, f"{ri:.10f}"))

                    res = self._ejecutar_pruebas(seq)
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

        try:
            if tipo == "Histograma":
                plt.figure(figsize=(9, 5))
                plt.hist(seq, bins=30, range=(0, 1), color="steelblue", edgecolor="black")
                plt.title(f"Histograma - {corrida}")
                plt.xlabel("Ri")
                plt.ylabel("Frecuencia")
                plt.grid(alpha=0.3)
                plt.tight_layout()
                plt.show()
            elif tipo == "Kolmogorov Smirnov":
                graficar_kolmogorov_smirnov(seq)
            elif tipo == "Poker":
                graficar_prueba_poker(seq)
            elif tipo == "Rachas":
                graficar_prueba_rachas(seq)
            elif tipo == "Chi Cuadrado":
                #k = max(10, min(100, len(seq) // 5))
                graficar_prueba_chi_cuadrado(seq, k=10, alpha=0.05)

            elif tipo == "Medias":
                if not self.secuencias:
                    raise ValueError("No hay corridas disponibles para graficar medias.")

                alpha = 0.05
                z = float(norm.ppf(1 - alpha / 2))

                sample_means = []
                ci_lower = []
                ci_upper = []

                for _, seq_i in self.secuencias.items():
                    n_i = len(seq_i)
                    if n_i < 2:
                        continue

                    media_i = float(np.mean(seq_i))
                    # IC centrado en la media muestral para mantener yerr >= 0.
                    error_i = z * ((1 / (12 * n_i)) ** 0.5)

                    sample_means.append(media_i)
                    ci_lower.append(media_i - error_i)
                    ci_upper.append(media_i + error_i)

                if not sample_means:
                    raise ValueError("No hay corridas con datos suficientes para graficar medias.")

                graficar_prueba_medias(
                    sample_means=sample_means,
                    ci_lower=ci_lower,
                    ci_upper=ci_upper,
                    theoretical_mean=0.5,
                    alpha=alpha,
                )

            elif tipo == "Varianza":
                if not self.secuencias:
                    raise ValueError("No hay corridas disponibles para graficar varianza.")

                alpha = 0.05
                var_teorica = 1 / 12

                sample_variances = []
                ci_lower = []
                ci_upper = []

                for _, seq_i in self.secuencias.items():
                    n_i = len(seq_i)
                    if n_i < 2:
                        continue

                    s2 = float(np.var(seq_i, ddof=1))
                    chi2_inf = float(chi2.ppf(alpha / 2, n_i - 1))
                    chi2_sup = float(chi2.ppf(1 - alpha / 2, n_i - 1))

                    li = (n_i - 1) * s2 / chi2_sup
                    ls = (n_i - 1) * s2 / chi2_inf

                    sample_variances.append(s2)
                    ci_lower.append(li)
                    ci_upper.append(ls)

                if not sample_variances:
                    raise ValueError("No hay corridas con datos suficientes para graficar varianza.")

                graficar_prueba_varianza(
                    sample_variances=sample_variances,
                    ci_lower=ci_lower,
                    ci_upper=ci_upper,
                    theoretical_variance=var_teorica,
                    alpha=alpha,
                )
        except Exception as e:
            messagebox.showerror("Error al graficar", str(e))

    def _exportar_treeview_csv(self, treeview, columnas, sugerido):
        path = filedialog.asksaveasfilename(
            title="Guardar CSV",
            defaultextension=".csv",
            initialfile=sugerido,
            filetypes=[("CSV", "*.csv")],
        )
        if not path:
            return

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(columnas)
            for item in treeview.get_children():
                writer.writerow(treeview.item(item)["values"])

        messagebox.showinfo("Exportacion", f"Archivo generado: {path}")

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

