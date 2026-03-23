from validadores.prueba_chi_cuadrado import PruebaChiCuadrado
from validadores.prueba_kolmogorov_smirnov import PruebaKolmogorovSmirnov
from validadores.prueba_medias import PruebaMedias
from validadores.prueba_varianza import PruebaVarianza
from validadores.prueba_poker import PruebaPoker
from validadores.prueba_rachas import PruebaRachas


class ValidacionService:
    @staticmethod
    def ejecutar_pruebas(seq, pruebas_activas):
        resultados = []

        for prueba in pruebas_activas:
            try:
                if prueba == "Chi Cuadrado":
                    k = max(10, min(100, len(seq) // 5))
                    ok = PruebaChiCuadrado().prueba_chi_cuadrado(seq, k=k)
                    resultados.append((prueba, ok, f"k={k}"))
                elif prueba == "Kolmogorov Smirnov":
                    ok = PruebaKolmogorovSmirnov().prueba_kolmogorov_smirnov(seq)
                    resultados.append((prueba, ok, "alpha=0.05"))
                elif prueba == "Medias":
                    ok = PruebaMedias().prueba_medias(seq)
                    resultados.append((prueba, ok, "alpha=0.05"))
                elif prueba == "Varianza":
                    ok = PruebaVarianza().prueba_varianza(seq)
                    resultados.append((prueba, ok, "alpha=0.05"))
                elif prueba == "Poker":
                    ok = PruebaPoker().prueba_poker(seq)
                    resultados.append((prueba, ok, "5 digitos"))
                elif prueba == "Rachas":
                    ok = PruebaRachas().prueba_rachas(seq)
                    resultados.append((prueba, ok, "mediana=0.5"))
            except Exception as e:
                resultados.append((prueba, False, f"Error: {e}"))

        return resultados
