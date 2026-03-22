import matplotlib.pyplot as plt
import numpy as np
from generador_numeros.congruencia_lineal import GeneradorCongruenciaLineal


def _graficar_histogramas(numeros, titulo, bins=50):
    """
    Dibuja dos histogramas de la misma secuencia:
    1. Escala normal
    2. Escala logaritmica

    Parameters
    ----------
    numeros : list[float]
        Secuencia de valores Ri en el intervalo [0, 1).
    titulo : str
        Titulo general de la figura.
    bins : int, optional
        Numero de intervalos del histograma.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    ax1.hist(
        numeros,
        bins=bins,
        range=(0, 1),
        color="steelblue",
        edgecolor="black",
        alpha=0.75
    )
    ax1.set_title("Vista Normal")
    ax1.set_xlabel("Valor (R_i)")
    ax1.set_ylabel("Frecuencia")
    ax1.set_xticks(np.arange(0, 1.05, 0.1))
    ax1.grid(axis="y", alpha=0.3)

    ax2.hist(
        numeros,
        bins=bins,
        range=(0, 1),
        color="coral",
        edgecolor="black",
        alpha=0.75
    )
    ax2.set_title("Escala Logaritmica")
    ax2.set_xlabel("Valor (R_i)")
    ax2.set_ylabel("Frecuencia (log)")
    ax2.set_xticks(np.arange(0, 1.05, 0.1))
    ax2.set_yscale("log")
    ax2.grid(axis="y", alpha=0.3, which="both")

    plt.suptitle(titulo, fontsize=12, fontweight="bold")
    plt.tight_layout()
    plt.show()


def visualizar_histograma_congruencia_lineal(semilla, pasos, bins=50):
    """
    Genera numeros pseudoaleatorios con el metodo de congruencia lineal
    y muestra su distribucion en histogramas.

    Formula del generador:
        X_(n+1) = (a * X_n + c) mod m
        R_i = X_i / m

    Parameters
    ----------
    semilla : int
        Valor inicial X0.
    pasos : int
        Cantidad de numeros Ri a generar.
    bins : int, optional
        Numero de intervalos para los histogramas.
    """
    gen = GeneradorCongruenciaLineal(semilla=semilla)
    numeros = gen.siguiente_Ri_Congruencia_Lineal(pasos)

    titulo = (
        "Histograma de Frecuencia - Congruencia Lineal\n"
        f"Semilla: {semilla}, Muestras: {pasos}"
    )

    print("\n--- Estadisticas ---")
    print(f"Total de numeros: {len(numeros)}")
    print(f'Lista de numeros: {numeros[:10]}{"..." if len(numeros) > 10 else ""}')
    print(f"Minimo: {min(numeros):.8f}")
    print(f"Maximo: {max(numeros):.8f}")
    print(f"Media: {sum(numeros)/len(numeros):.8f}")
    print("Esperado (uniforme [0,1)): 0.5")

    _graficar_histogramas(numeros, titulo, bins=bins)
