import matplotlib.pyplot as plt
import numpy as np
from generador_numeros.congruencial_multiplicativo import GeneradorCongruencialMultiplicativo


def _graficar_histogramas(numeros, titulo, bins=50):
    """
    Dibuja dos histogramas de la misma secuencia:
    1) escala normal
    2) escala logaritmica (util para ver frecuencias pequenas)

    Parameters
    ----------
    numeros : list[float]
        Secuencia de valores Ri en [0, 1).
    titulo : str
        Titulo general de la figura.
    bins : int, optional
        Cantidad de intervalos del histograma.
    """
    # Creamos una figura con dos paneles horizontales
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
    # Ayuda cuando hay barras muy altas que esconden las barras pequenas
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

    # Titulo global y ajuste de espacios
    plt.suptitle(titulo, fontsize=12, fontweight="bold")
    plt.tight_layout()
    plt.show()


def visualizar_histograma_congruencial_multiplicativo(
    semilla, pasos, a=1664525, m=2**32, bins=50
):
    """
    Genera numeros pseudoaleatorios con el metodo congruencial multiplicativo
    y muestra su distribucion en histogramas.

    Formula del generador:
        X_(n+1) = (a * X_n) mod m
        R_i = X_i / m

    Parameters
    ----------
    semilla : int
        Valor inicial X0.
    pasos : int
        Cantidad de numeros a generar.
    a : int, optional
        Multiplicador del metodo.
    m : int, optional
        Modulo del metodo.
    bins : int, optional
        Cantidad de intervalos para el histograma.
    """
    # Instanciamos el generador con los parametros elegidos
    gen = GeneradorCongruencialMultiplicativo(semilla=semilla, a=a, m=m)

    # Generamos la secuencia Ri
    numeros = gen.siguiente_Ri_Congruencial_Multiplicativo(pasos)

    # Construimos titulo descriptivo para la grafica
    titulo = (
        "Histograma de Frecuencia - Congruencial Multiplicativo\n"
        f"Semilla: {semilla}, a: {a}, m: {m}, Muestras: {pasos}"
    )

    # Resumen numerico en consola para validar rapidamente resultados
    print("\n--- Estadisticas ---")
    print(f"Total de numeros: {len(numeros)}")
    print(f'Lista de numeros: {numeros[:10]}{"..." if len(numeros) > 10 else ""}')
    print(f"Minimo: {min(numeros):.8f}")
    print(f"Maximo: {max(numeros):.8f}")
    print(f"Media: {sum(numeros)/len(numeros):.8f}")
    print("Esperado (uniforme [0,1)): 0.5")

    # Mostramos la visualizacion
    _graficar_histogramas(numeros, titulo, bins=bins)

