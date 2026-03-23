from validadores.prueba_chi_cuadrado import PruebaChiCuadrado
from validadores.prueba_kolmogorov_smirnov import PruebaKolmogorovSmirnov
from validadores.prueba_medias import PruebaMedias
from validadores.prueba_varianza import PruebaVarianza
from validadores.prueba_poker import PruebaPoker
from validadores.prueba_rachas import PruebaRachas
from statistics import NormalDist


class ValidacionService:
    _NORMAL_STD = NormalDist(mu=0.0, sigma=1.0)

    @staticmethod
    def _transformar_para_validacion(seq, metodo=None, params_dist=None):
        """Transforma secuencias de distribuciones a U(0,1) para validar con pruebas actuales."""
        if metodo == "Distribucion Uniforme":
            if not params_dist:
                return seq
            a = float(params_dist.get("a", 0.0))
            b = float(params_dist.get("b", 1.0))
            if a >= b:
                raise ValueError("Para validar distribución uniforme debe cumplirse a < b.")
            amplitud = b - a
            return [min(max((float(x) - a) / amplitud, 0.0), 1.0 - 1e-12) for x in seq]

        if metodo == "Distribucion Normal":
            if not params_dist:
                return seq
            mu = float(params_dist.get("mu", 0.0))
            sigma = float(params_dist.get("sigma", 1.0))
            if sigma <= 0:
                raise ValueError("Para validar distribución normal, sigma debe ser mayor que 0.")
            return [
                min(max(ValidacionService._NORMAL_STD.cdf((float(x) - mu) / sigma), 1e-12), 1.0 - 1e-12)
                for x in seq
            ]

        return seq

    @staticmethod
    def ejecutar_pruebas(seq, pruebas_activas, metodo=None, params_dist=None):
        seq_validacion = ValidacionService._transformar_para_validacion(
            seq, metodo=metodo, params_dist=params_dist
        )
        resultados = []

        for prueba in pruebas_activas:
            try:
                if prueba == "Chi Cuadrado":
                    k = max(10, min(100, len(seq_validacion) // 5))
                    ok = PruebaChiCuadrado().prueba_chi_cuadrado(seq_validacion, k=k)
                    resultados.append((prueba, ok, f"k={k}"))
                elif prueba == "Kolmogorov Smirnov":
                    ok = PruebaKolmogorovSmirnov().prueba_kolmogorov_smirnov(seq_validacion)
                    resultados.append((prueba, ok, "alpha=0.05"))
                elif prueba == "Medias":
                    ok = PruebaMedias().prueba_medias(seq_validacion)
                    resultados.append((prueba, ok, "alpha=0.05"))
                elif prueba == "Varianza":
                    ok = PruebaVarianza().prueba_varianza(seq_validacion)
                    resultados.append((prueba, ok, "alpha=0.05"))
                elif prueba == "Poker":
                    ok = PruebaPoker().prueba_poker(seq_validacion)
                    resultados.append((prueba, ok, "5 digitos"))
                elif prueba == "Rachas":
                    ok = PruebaRachas().prueba_rachas(seq_validacion)
                    resultados.append((prueba, ok, "mediana=0.5"))
            except Exception as e:
                resultados.append((prueba, False, f"Error: {e}"))

        return resultados
