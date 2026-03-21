class GeneradorCongruencialAditivo:
    """
    Generador de números pseudoaleatorios usando método congruencial aditivo.

    Fórmula base (orden 2):
        X_n = (X_{n-1} + X_{n-2}) mod m

    Normalización:
        R_i = X_i / m

    Notas:
    - Se requieren al menos 2 semillas iniciales.
    - El método es determinista: mismas semillas y mismo m => misma secuencia.
    """

    def __init__(self, semillas_iniciales, m=2**32):
        if len(semillas_iniciales) < 2:
            raise ValueError("Debes proporcionar al menos 2 semillas iniciales.")
        if any(s < 0 for s in semillas_iniciales):
            raise ValueError("Todas las semillas deben ser no negativas.")
        if m <= 0:
            raise ValueError("El módulo m debe ser mayor que 0.")

        self.estado = [int(s) % m for s in semillas_iniciales]
        self.m = m

    def _siguiente_xi(self):
        # Usa las dos últimas semillas del estado
        xi = (self.estado[-1] + self.estado[-2]) % self.m
        self.estado.append(xi)
        return xi

    def siguiente_Ri_Congruencial_Aditivo(self, pasos: int):
        if pasos <= 0:
            return []

        secuencia_Ri = []
        for _ in range(pasos):
            xi = self._siguiente_xi()
            ri = xi / self.m
            secuencia_Ri.append(ri)

        return secuencia_Ri