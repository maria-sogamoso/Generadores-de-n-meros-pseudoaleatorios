class GeneradorCuadradosMedios:
    """
    Generador de números pseudoaleatorios por el método de cuadrados medios.

    Método:
        X_{n+1} = extracción de los dígitos centrales de (X_n)^2
        R_i = X_i / 10^d
    donde d es la cantidad de dígitos usada en la semilla.
    """

    def __init__(self, semilla: int, digitos: int = 8):
        if digitos % 2 != 0:
            raise ValueError("digitos debe ser par (ej. 4, 6, 8).")
        if semilla < 0:
            raise ValueError("semilla debe ser no negativa.")
        if semilla >= 10**digitos:
            raise ValueError(
                f"semilla debe tener como máximo {digitos} dígitos."
            )

        self.semilla = semilla
        self.digitos = digitos
        self.base_normalizacion = 10**digitos

    def _siguiente_xi(self) -> int:
        cuadrado = self.semilla * self.semilla

        # Rellenar con ceros para asegurar longitud 2d
        cadena = str(cuadrado).zfill(2 * self.digitos)

        # Tomar los d dígitos centrales
        inicio = self.digitos // 2
        fin = inicio + self.digitos
        xi = int(cadena[inicio:fin])

        self.semilla = xi
        return xi

    def siguiente_Ri_Cuadrados_Medios(self, pasos: int):
        if pasos <= 0:
            return []

        secuencia_Ri = []
        for _ in range(pasos):
            xi = self._siguiente_xi()
            ri = xi / self.base_normalizacion
            secuencia_Ri.append(ri)

        return secuencia_Ri