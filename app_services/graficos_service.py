import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2, norm

from visualizaciones.graficas_de_validacion import (
    graficar_kolmogorov_smirnov,
    graficar_prueba_chi_cuadrado,
    graficar_prueba_poker,
    graficar_prueba_rachas,
    graficar_prueba_medias,
    graficar_prueba_varianza,
)


class GraficosService:
    @staticmethod
    def mostrar(tipo, corrida, seq, secuencias):
        if tipo == "Histograma":
            plt.figure(figsize=(9, 5))
            plt.hist(seq, bins=30, range=(0, 1), color="steelblue", edgecolor="black")
            plt.title(f"Histograma - {corrida}")
            plt.xlabel("Ri")
            plt.ylabel("Frecuencia")
            plt.grid(alpha=0.3)
            plt.tight_layout()
            plt.show()
            return

        if tipo == "Kolmogorov Smirnov":
            graficar_kolmogorov_smirnov(seq)
            return

        if tipo == "Poker":
            graficar_prueba_poker(seq)
            return

        if tipo == "Rachas":
            graficar_prueba_rachas(seq)
            return

        if tipo == "Chi Cuadrado":
            graficar_prueba_chi_cuadrado(seq, k=10, alpha=0.05)
            return

        if tipo == "Medias":
            GraficosService._graficar_medias(secuencias)
            return

        if tipo == "Varianza":
            GraficosService._graficar_varianza(secuencias)

    @staticmethod
    def _graficar_medias(secuencias):
        if not secuencias:
            raise ValueError("No hay corridas disponibles para graficar medias.")

        alpha = 0.05
        z = float(norm.ppf(1 - alpha / 2))

        sample_means = []
        ci_lower = []
        ci_upper = []

        for seq_i in secuencias.values():
            n_i = len(seq_i)
            if n_i < 2:
                continue

            media_i = float(np.mean(seq_i))
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

    @staticmethod
    def _graficar_varianza(secuencias):
        if not secuencias:
            raise ValueError("No hay corridas disponibles para graficar varianza.")

        alpha = 0.05
        var_teorica = 1 / 12

        sample_variances = []
        ci_lower = []
        ci_upper = []

        for seq_i in secuencias.values():
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
