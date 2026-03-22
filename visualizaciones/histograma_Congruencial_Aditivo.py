import matplotlib.pyplot as plt
import numpy as np
from generador_numeros.congruencial_aditivo import GeneradorCongruencialAditivo


def _graficar_histogramas(numeros, titulo, bins=50):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Vista normal
    ax1.hist(
        numeros, bins=bins, range=(0, 1),
        color="steelblue", edgecolor="black", alpha=0.75
    )
    ax1.set_title("Vista Normal")
    ax1.set_xlabel("Valor (R_i)")
    ax1.set_ylabel("Frecuencia")
    ax1.set_xticks(np.arange(0, 1.05, 0.1))
    ax1.grid(axis="y", alpha=0.3)

    # Vista log
    ax2.hist(
        numeros, bins=bins, range=(0, 1),
        color="coral", edgecolor="black", alpha=0.75
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


def visualizar_histograma_congruencial_aditivo(semillas_iniciales, pasos, m=2**32, bins=50):
    gen = GeneradorCongruencialAditivo(semillas_iniciales=semillas_iniciales, m=m)
    numeros = gen.siguiente_Ri_Congruencial_Aditivo(pasos)

    titulo = (
        "Histograma de Frecuencia - Congruencial Aditivo\n"
        f"Semillas: {semillas_iniciales}, m: {m}, Muestras: {pasos}"
    )
    
    print("\n--- Estadisticas ---")
    print(f"Total de numeros: {len(numeros)}")
    print(f'Lista de numeros: {numeros[:10]}{"..." if len(numeros) > 10 else ""}')
    print(f"Minimo: {min(numeros):.8f}")
    print(f"Maximo: {max(numeros):.8f}")
    print(f"Media: {sum(numeros)/len(numeros):.8f}")
    print("Esperado (uniforme [0,1)): 0.5")

    _graficar_histogramas(numeros, titulo, bins=bins)
