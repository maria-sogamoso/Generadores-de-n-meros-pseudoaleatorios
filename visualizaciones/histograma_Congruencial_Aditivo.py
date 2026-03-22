import matplotlib.pyplot as plt
import numpy as np
from generador_numeros.congruencial_aditivo import GeneradorCongruencialAditivo


def _graficar_histogramas(numeros, titulo, bins=50):
    """
    Dibuja dos histogramas de la misma secuencia:
    1. Escala normal
    2. Escala logaritmica (para resaltar frecuencias pequenas)

    Parameters
    ----------
    numeros : list[float]
        Secuencia de valores Ri en el intervalo [0, 1).
    titulo : str
        Titulo general que se mostrara en la figura.
    bins : int, optional
        Numero de intervalos del histograma.
    """
    # Figura con dos paneles (normal y log)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Histograma en escala normal
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

    # Histograma en escala logaritmica
    # Util cuando una barra domina y oculta las demas
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

    # Titulo global de la figura
    plt.suptitle(titulo, fontsize=12, fontweight="bold")
    plt.tight_layout()
    plt.show()


def visualizar_histograma_congruencial_aditivo(semillas_iniciales, pasos, m=2**32, bins=50):
    """
    Genera numeros pseudoaleatorios con el metodo congruencial aditivo
    y muestra su distribucion en histogramas.

    Metodo usado:
        X_n = (X_{n-1} + X_{n-2}) mod m
        R_i = X_i / m

    Parameters
    ----------
    semillas_iniciales : list[int] | tuple[int, ...]
        Valores iniciales del generador (se requieren al menos 2).
    pasos : int
        Cantidad de numeros Ri a generar.
    m : int, optional
        Modulo del generador. Por defecto 2**32.
    bins : int, optional
        Numero de intervalos para los histogramas.
    """
    # Crear generador y producir secuencia
    gen = GeneradorCongruencialAditivo(semillas_iniciales=semillas_iniciales, m=m)
    numeros = gen.siguiente_Ri_Congruencial_Aditivo(pasos)

    # Titulo descriptivo para la grafica
    titulo = (
        "Histograma de Frecuencia - Congruencial Aditivo\n"
        f"Semillas: {semillas_iniciales}, m: {m}, Muestras: {pasos}"
    )

    # Resumen estadistico en consola
    print("\n--- Estadisticas ---")
    print(f"Total de numeros: {len(numeros)}")
    print(f'Lista de numeros: {numeros[:10]}{"..." if len(numeros) > 10 else ""}')
    print(f"Minimo: {min(numeros):.8f}")
    print(f"Maximo: {max(numeros):.8f}")
    print(f"Media: {sum(numeros)/len(numeros):.8f}")
    print("Esperado (uniforme [0,1)): 0.5")

    # Mostrar histogramas
    _graficar_histogramas(numeros, titulo, bins=bins)

