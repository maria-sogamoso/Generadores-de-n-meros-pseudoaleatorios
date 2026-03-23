from generador_numeros.cuadrados_medios import GeneradorCuadradosMedios
from generador_numeros.congruencia_lineal import GeneradorCongruenciaLineal
from generador_numeros.congruencial_multiplicativo import GeneradorCongruencialMultiplicativo
from generador_numeros.congruencial_aditivo import GeneradorCongruencialAditivo


class GeneracionService:
    @staticmethod
    def generar_por_metodo(metodo, semillas, pasos, corridas=1, digitos=8, a_mult=1664525, m=2**32):
        corridas_generadas = {}

        if metodo == "Cuadrados Medios":
            for s in semillas:
                for i in range(corridas):
                    semilla_i = s + i
                    gen = GeneradorCuadradosMedios(semilla=semilla_i, digitos=digitos)
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
            for s in semillas:
                for i in range(corridas):
                    semilla_i = s + i
                    gen = GeneradorCongruencialMultiplicativo(
                        semilla=semilla_i,
                        a=a_mult,
                        m=m,
                    )
                    seq = gen.siguiente_Ri_Congruencial_Multiplicativo(pasos)
                    key = f"{metodo} | corrida={i + 1} | semilla={semilla_i}"
                    corridas_generadas[key] = (metodo, semilla_i, seq)

        elif metodo == "Congruencial Aditivo":
            if len(semillas) < 2:
                raise ValueError("Congruencial aditivo requiere al menos 2 semillas.")
            for i in range(corridas):
                semillas_i = [s + i for s in semillas]
                gen = GeneradorCongruencialAditivo(semillas_iniciales=semillas_i, m=m)
                seq = gen.siguiente_Ri_Congruencial_Aditivo(pasos)
                key = f"{metodo} | corrida={i + 1} | semillas={semillas_i}"
                corridas_generadas[key] = (metodo, f"lista+{i}", seq)

        return corridas_generadas
