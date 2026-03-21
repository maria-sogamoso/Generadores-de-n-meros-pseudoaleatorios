class GeneradorCongruencialMultiplicativo:
    """
    Generador de números pseudoaleatorios usando método congruencial multiplicativo.

    Fórmula:
        X_{n+1} = (a * X_n) mod m

    Normalización:
        R_i = X_i / m

    Notas:
    - Se requiere semilla inicial X_0 > 0.
    - El método es determinista: misma semilla y mismos parámetros => misma secuencia.
    """

    def __init__(self, semilla: int, a: int = 1664525, m: int = 2**32):
        if semilla <= 0:
            raise ValueError("semilla debe ser mayor que 0.")
        if a <= 0:
            raise ValueError("a (multiplicador) debe ser mayor que 0.")
        if m <= 0:
            raise ValueError("m (módulo) debe ser mayor que 0.")

        self.semilla = semilla % m
        self.a = a
        self.m = m

    def _siguiente_xi(self) -> int:
        xi = (self.a * self.semilla) % self.m
        self.semilla = xi
        return xi

    def siguiente_Ri_Congruencial_Multiplicativo(self, pasos: int):
        if pasos <= 0:
            return []

        secuencia_Ri = []
        for _ in range(pasos):
            xi = self._siguiente_xi()
            ri = xi / self.m
            secuencia_Ri.append(ri)

        return secuencia_Ri