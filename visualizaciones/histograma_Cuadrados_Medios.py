import matplotlib.pyplot as plt
import numpy as np
from generador_numeros.cuadrados_medios import GeneradorCuadradosMedios


def visualizar_histograma_cuadrados_medios(semilla, digitos, pasos, bins=50):
    """
    Genera números pseudoaleatorios con cuadrados medios y los visualiza en dos histogramas.
    """
    gen = GeneradorCuadradosMedios(semilla=semilla, digitos=digitos)
    numeros = gen.siguiente_Ri_Cuadrados_Medios(pasos)

    # Crear dos subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Histograma 1: Normal
    ax1.hist(numeros, bins=bins, range=(0, 1), color='steelblue', edgecolor='black', alpha=0.7)
    ax1.set_xlabel('Valor (R_i)')
    ax1.set_ylabel('Frecuencia')
    ax1.set_title('Vista Normal')
    ax1.set_xticks(np.arange(0, 1.05, 0.1))
    ax1.grid(axis='y', alpha=0.3)

    # Histograma 2: Escala logarítmica
    ax2.hist(numeros, bins=bins, range=(0, 1), color='coral', edgecolor='black', alpha=0.7)
    ax2.set_xlabel('Valor (R_i)')
    ax2.set_ylabel('Frecuencia (escala log)')
    ax2.set_title('Escala Logarítmica')
    ax2.set_xticks(np.arange(0, 1.05, 0.1))
    ax2.set_yscale('log')
    ax2.grid(axis='y', alpha=0.3, which='both')

    plt.suptitle(f'Histograma de Frecuencia - Cuadrados Medios\n'
                 f'Semilla: {semilla}, Dígitos: {digitos}, Muestras: {pasos}', 
                 fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.show()

    # Estadísticas básicas
    print(f"\n--- Estadísticas ---")
    print(f"Total de números: {len(numeros)}")
    print(f"Mínimo: {min(numeros):.8f}")
    print(f"Máximo: {max(numeros):.8f}")
    print(f"Media: {sum(numeros)/len(numeros):.8f}")
    print(f"Esperado (uniforme [0,1)): 0.5")