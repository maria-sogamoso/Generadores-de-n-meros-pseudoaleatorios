import matplotlib.pyplot as plt
import numpy as np
from generador_numeros.cuadrados_medios import GeneradorCuadradosMedios


def _graficar_histogramas(numeros, titulo, bins=50):
    """
    Dibuja dos histogramas de la misma secuencia:
    1. Escala normal.
    2. Escala logarítmica (util para ver frecuencias pequenas).

    Parameters
    ----------
    numeros : list[float]
        Secuencia de valores Ri en [0, 1).
    titulo : str
        Titulo global de la figura.
    bins : int, optional
        Cantidad de intervalos del histograma.
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
        alpha=0.7
    )
    ax1.set_xlabel("Valor (R_i)")
    ax1.set_ylabel("Frecuencia")
    ax1.set_title("Vista Normal")
    ax1.set_xticks(np.arange(0, 1.05, 0.1))
    ax1.grid(axis="y", alpha=0.3)

    # Histograma en escala logarítmica
    # Ayuda cuando una barra muy alta tapa las demas
    ax2.hist(
        numeros,
        bins=bins,
        range=(0, 1),
        color="coral",
        edgecolor="black",
        alpha=0.7
    )
    ax2.set_xlabel("Valor (R_i)")
    ax2.set_ylabel("Frecuencia (escala log)")
    ax2.set_title("Escala Logarítmica")
    ax2.set_xticks(np.arange(0, 1.05, 0.1))
    ax2.set_yscale("log")
    ax2.grid(axis="y", alpha=0.3, which="both")

    # Titulo general y ajuste de espacios
    plt.suptitle(titulo, fontsize=12, fontweight="bold")
    plt.tight_layout()
    plt.show()


def visualizar_histograma_cuadrados_medios(semilla, digitos, pasos, bins=50):
    """
    Genera numeros pseudoaleatorios con el metodo de cuadrados medios
    y muestra su distribucion en histogramas.

    Metodo:
        X_{n+1} = extraccion de digitos centrales de (X_n)^2
        R_i = X_i / 10^d

    Parameters
    ----------
    semilla : int
        Valor inicial X_0.
    digitos : int
        Cantidad de digitos de trabajo (debe ser par).
    pasos : int
        Cantidad de numeros a generar.
    bins : int, optional
        Cantidad de intervalos para los histogramas.
    """
    # Crear generador y producir secuencia Ri
    gen = GeneradorCuadradosMedios(semilla=semilla, digitos=digitos)
    numeros = gen.siguiente_Ri_Cuadrados_Medios(pasos)

    # Titulo descriptivo para la visualizacion
    titulo = (
        "Histograma de Frecuencia - Cuadrados Medios\n"
        f"Semilla: {semilla}, Digitos: {digitos}, Muestras: {pasos}"
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

