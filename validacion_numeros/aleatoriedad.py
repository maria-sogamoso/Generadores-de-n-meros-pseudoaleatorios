from scipy.stats import chi2, norm  # type: ignore


class RandomnessTest:
    def prueba_medias(self, numeros_aleatorios):
        """
        Prueba de medias usando distribución normal (Z).

        Se verifica si la media calculada está dentro del intervalo:
        LLR = 0.5 - Z_α/2 * (1/√12n)
        LSR = 0.5 + Z_α/2 * (1/√12n)
        """
        n = len(numeros_aleatorios)
        media_calculada = sum(numeros_aleatorios) / n
        media_teorica = 0.5

        alpha = 0.05  # Nivel de aceptación (95% de confianza)

        # Valor crítico Z para la distribución normal
        Z_alpha_2 = norm.ppf(1 - alpha / 2)  # 1.96 para α=0.05

        # Límites
        desviacion = (1 / (12 * n)) ** 0.5
        LLR = media_teorica - Z_alpha_2 * desviacion
        LSR = media_teorica + Z_alpha_2 * desviacion

        if LLR <= media_calculada <= LSR:
            print("Prueba de medias: Aceptada")
            print(f"  Media calculada: {media_calculada:.8f}")
            print(f"  Rango: [{LLR:.8f}, {LSR:.8f}]")
            return True
        else:
            print("Prueba de medias: Rechazada")
            print(f"  Media calculada: {media_calculada:.8f}")
            print(f"  Rango: [{LLR:.8f}, {LSR:.8f}]")
            return False

    def prueba_varianza(self, numeros_aleatorios):
        """
        Prueba de varianza para números pseudoaleatorios [0,1].

        Se verifica si la varianza calculada está dentro del intervalo:
        LLR = chi2_alpha_2 / (12 * (n - 1))
        LSR = chi2_1_minus_alpha_2 / (12 * (n - 1))
        """
        n = len(numeros_aleatorios)
        alpha = 0.05  # Nivel de significancia (5%)

        # 1. Calcular Media y Varianza
        media_calculada = sum(numeros_aleatorios) / n
        varianza_calculada = sum(
            (x - media_calculada) ** 2 for x in numeros_aleatorios
        ) / (n - 1)

        # 2. Valores críticos de Chi-cuadrado / chi2.ppf usa la probabilidad acumulada a la izquierda
        chi2_alpha_2 = chi2.ppf(1 - alpha / 2, n - 1)
        chi2_1_minus_alpha_2 = chi2.ppf(alpha / 2, n - 1)

        # 3. Límites de Aceptación
        LLR = chi2_alpha_2 / (12 * (n - 1))
        LSR = chi2_1_minus_alpha_2 / (12 * (n - 1))

        # 4. Comparamos la varianza directamente contra los límites
        if LSR <= varianza_calculada <= LLR:
            print("Prueba de varianza: Aceptada")
            print(f"  Varianza calculada: {varianza_calculada:.8f}")
            print(f"  Rango: [{LSR:.8f}, {LLR:.8f}]")
            cumple = True
        else:
            print("Prueba de varianza: Rechazada")
            print(f"  Varianza calculada: {varianza_calculada:.8f}")
            print(f"  Rango: [{LSR:.8f}, {LLR:.8f}]")
            cumple = False

        return cumple
