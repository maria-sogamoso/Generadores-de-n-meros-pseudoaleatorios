import math

import numpy as np
from scipy.stats import chi2, ksone  # type: ignore


class PruebaUniformidad:
    def prueba_chi_cuadrado(self, numeros_aleatorios, k=1000):
        n = len(numeros_aleatorios)
        if n == 0:
            print("No se pueden realizar pruebas con una lista vacía.")
            return False

        # 1. Dividir el rango [0, 1) en k intervalos iguales
        # 2. Contar cuántos números caen en cada intervalo
        frecuencias_observadas, _ = np.histogram(
            numeros_aleatorios, bins=k, range=(0, 1)
        )

        # 3. Calcular la frecuencia esperada (n/k para cada intervalo)
        frecuencia_esperada = n / k

        # 4. Calcular el estadístico de chi-cuadrado
        chi_cuadrado_calculado = sum(
            (fo - frecuencia_esperada) ** 2 / frecuencia_esperada
            for fo in frecuencias_observadas
        )

        # 5. Obtener el valor crítico de chi-cuadrado para k-1 grados de libertad y un nivel de significancia (alpha=0.05)

        alpha = 0.05
        grados_libertad = k - 1
        chi_cuadrado_teorico = chi2.ppf(1 - alpha, grados_libertad)

        # 6. Comparar el estadístico calculado con el valor teórico
        if chi_cuadrado_calculado < chi_cuadrado_teorico:
            print("Prueba de chi-cuadrado: Aceptada")
            print(f"  Chi-cuadrado calculado: {chi_cuadrado_calculado:.8f}")
            print(f"  Chi-cuadrado teórico: {chi_cuadrado_teorico:.8f}")
            return True
        else:
            print("Prueba de chi-cuadrado: Rechazada")
            print(f"  Chi-cuadrado calculado: {chi_cuadrado_calculado:.8f}")
            print(f"  Chi-cuadrado teórico: {chi_cuadrado_teorico:.8f}")
            return False

    def prueba_kolmogorov_smirnov(self, numeros_aleatorios, alpha=0.05):
        n = len(numeros_aleatorios)
        datos_ordenados = sorted(numeros_aleatorios)

        d_max = 0
        for i in range(1, n + 1):
            # Frecuencia acumulada real
            f_observada = i / n
            # Frecuencia acumulada teórica para distribución uniforme
            f_teorica = datos_ordenados[i - 1]

            # Calculamos la diferencia absoluta
            distancia = abs(f_observada - f_teorica)

            if distancia > d_max:
                d_max = distancia

        # 3. Obtener el Valor Crítico (D-Alfa)
        # Para n > 50, se suele usar la aproximación: 1.36 / sqrt(n) para alpha=0.05
        if n > 50:
            d_critico = 1.36 / math.sqrt(n)
        else:
            # Para muestras pequeñas, usamos el valor de la distribución ksone (Kolmogorov-Smirnov)
            d_critico = ksone.ppf(1 - alpha / 2, n)

        # 4. Verificación
        aceptada = d_max < d_critico

        print(f"  D-Max calculado: {d_max:.5f}")
        print(f"  D-Teórico (D-alfa): {d_critico:.5f}")
        print(f"  Resultado: {'Aceptada' if aceptada else 'Rechazada'}")

        return aceptada
