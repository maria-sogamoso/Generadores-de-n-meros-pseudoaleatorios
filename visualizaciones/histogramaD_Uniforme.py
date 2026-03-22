import matplotlib.pyplot as plt
import numpy as np
from distribuciones.uniforme import GeneradorDistribucionUniforme
from generador_numeros.congruencia_lineal import GeneradorCongruenciaLineal


def _graficar_histogramas(numeros, titulo, a, b, bins=50):
    """
    Dibuja dos histogramas de la misma secuencia:
    1. Escala normal
    2. Escala logaritmica

    Parameters
    ----------
    numeros : list[float]
        Secuencia de valores U(a, b).
    titulo : str
        Titulo general de la figura.
    a : float
        Limite inferior de la distribucion uniforme.
    b : float
        Limite superior de la distribucion uniforme.
    bins : int, optional
        Numero de intervalos del histograma.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    ax1.hist(
        numeros,
        bins=bins,
        range=(a, b),
        color="steelblue",
        edgecolor="black",
        alpha=0.75
    )
    ax1.set_title("Vista Normal")
    ax1.set_xlabel("Valor")
    ax1.set_ylabel("Frecuencia")
    ax1.set_xticks(np.linspace(a, b, 11))
    ax1.grid(axis="y", alpha=0.3)

    ax2.hist(
        numeros,
        bins=bins,
        range=(a, b),
        color="coral",
        edgecolor="black",
        alpha=0.75
    )
    ax2.set_title("Escala Logaritmica")
    ax2.set_xlabel("Valor")
    ax2.set_ylabel("Frecuencia (log)")
    ax2.set_xticks(np.linspace(a, b, 11))
    ax2.set_yscale("log")
    ax2.grid(axis="y", alpha=0.3, which="both")

    plt.suptitle(titulo, fontsize=12, fontweight="bold")
    plt.tight_layout()
    plt.show()


def visualizar_histograma_distribucion_uniforme(
    semilla,
    pasos,
    a=0.0,
    b=1.0,
    bins=50,
):
    """
    Genera una muestra con distribucion uniforme U(a, b)
    y muestra su distribucion en histogramas.

    Flujo de generacion:
        1) Generar base uniforme U(0,1) con Congruencia Lineal.
        2) Transformar al intervalo [a, b) con transformada inversa.

    Parameters
    ----------
    semilla : int
        Semilla para el generador congruencial lineal.
    pasos : int
        Cantidad de valores a generar.
    a : float, optional
        Limite inferior de la distribucion uniforme objetivo.
    b : float, optional
        Limite superior de la distribucion uniforme objetivo.
    bins : int, optional
        Numero de intervalos para los histogramas.
    """
    gen_base = GeneradorCongruenciaLineal(semilla=semilla)
    uniformes_base = gen_base.siguiente_Ri_Congruencia_Lineal(pasos)

    gen_uniforme = GeneradorDistribucionUniforme(a=a, b=b)
    numeros = gen_uniforme.generar(uniformes_base)

    titulo = (
        "Histograma de Frecuencia - Distribucion Uniforme\n"
        f"Semilla: {semilla}, a: {a}, b: {b}, Muestras: {pasos}"
    )

    print("\n--- Estadisticas ---")
    print(f"Total de numeros: {len(numeros)}")
    print(f'Lista de numeros: {numeros[:10]}{"..." if len(numeros) > 10 else ""}')
    print(f"Minimo: {min(numeros):.8f}")
    print(f"Maximo: {max(numeros):.8f}")
    print(f"Media: {sum(numeros)/len(numeros):.8f}")
    print(f"Esperado (uniforme [{a}, {b})): {(a + b) / 2:.8f}")

    _graficar_histogramas(numeros, titulo, a=a, b=b, bins=bins)
