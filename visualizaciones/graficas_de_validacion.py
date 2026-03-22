import math
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ksone, norm  # type: ignore


def graficar_kolmogorov_smirnov(numeros_aleatorios, alpha=0.05):
    """
    Grafica la Funcion Empirica Acumulada (FEC) contra la distribucion
    teorica uniforme y resalta la maxima diferencia (estadistico D).

    Parameters
    ----------
    numeros_aleatorios : list[float]
        Muestra de numeros pseudoaleatorios en [0, 1).
    alpha : float, optional
        Nivel de significancia para calcular D critico.

    Returns
    -------
    dict
        Resumen con d_max, d_critico, aceptada y posicion de la maxima
        diferencia.
    """
    if not numeros_aleatorios:
        raise ValueError("La lista de numeros no puede estar vacia.")

    n = len(numeros_aleatorios)
    datos_ordenados = np.sort(np.asarray(numeros_aleatorios, dtype=float))

    # FEC: i/n para cada observacion ordenada x_i.
    fec = np.arange(1, n + 1) / n

    # Para U(0,1), F_teorica(x_i) = x_i.
    f_teorica = datos_ordenados
    diferencias = np.abs(fec - f_teorica)

    idx_max = int(np.argmax(diferencias))
    d_max = float(diferencias[idx_max])

    if n > 50:
        d_critico = 1.36 / math.sqrt(n)
    else:
        d_critico = float(ksone.ppf(1 - alpha / 2, n))

    aceptada = d_max < d_critico

    plt.figure(figsize=(10, 6))

    # Curva teorica de la uniforme: F(x) = x.
    x_ref = np.linspace(0, 1, 200)
    plt.plot(x_ref, x_ref, label="F teorica U(0,1)", color="black", linewidth=2)

    # FEC como funcion escalonada.
    plt.step(datos_ordenados, fec, where="post", label="FEC", color="steelblue")

    x_d = float(datos_ordenados[idx_max])
    y_emp = float(fec[idx_max])
    y_teo = float(f_teorica[idx_max])

    plt.vlines(
        x_d,
        min(y_emp, y_teo),
        max(y_emp, y_teo),
        colors="crimson",
        linewidth=2,
        label=f"D max = {d_max:.5f}",
    )

    plt.title("Prueba Kolmogorov-Smirnov: FEC vs Teorica Uniforme")
    plt.xlabel("x")
    plt.ylabel("F(x)")
    plt.xlim(0, 1)
    plt.ylim(0, 1.02)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

    print("\n--- Resumen KS ---")
    print(f"D max: {d_max:.5f}")
    print(f"D critico: {d_critico:.5f}")
    print(f"Resultado: {'Aceptada' if aceptada else 'Rechazada'}")

    return {
        "d_max": d_max,
        "d_critico": d_critico,
        "aceptada": aceptada,
        "x_d": x_d,
    }


def _clasificar_categoria_poker(digitos):
    distintos = len(set(digitos))

    if distintos == 5:
        return "Todos Diferentes"
    if distintos == 1:
        return "Quintilla"

    conteos = sorted(Counter(digitos).values(), reverse=True)

    if distintos == 4:
        return "Un Par"
    if distintos == 3:
        return "Tercia" if conteos[0] == 3 else "Dos Pares"
    if distintos == 2:
        return "Poker" if conteos[0] == 4 else "Full House"

    return "Todos Diferentes"


def graficar_prueba_poker(numeros_aleatorios):
    """
    Grafica frecuencias observadas vs esperadas por categoria de la
    prueba de Poker.

    Parameters
    ----------
    numeros_aleatorios : list[float]
        Muestra de numeros pseudoaleatorios en [0, 1).

    Returns
    -------
    dict
        Frecuencias observadas/esperadas por categoria.
    """
    if not numeros_aleatorios:
        raise ValueError("La lista de numeros no puede estar vacia.")

    n = len(numeros_aleatorios)
    poker_numeros = [f"{num:.5f}"[2:] for num in numeros_aleatorios]

    categorias = [
        "Todos Diferentes",
        "Un Par",
        "Dos Pares",
        "Tercia",
        "Full House",
        "Poker",
        "Quintilla",
    ]

    probabilidades = {
        "Todos Diferentes": 0.30240,
        "Un Par": 0.50400,
        "Dos Pares": 0.10800,
        "Tercia": 0.07200,
        "Full House": 0.00900,
        "Poker": 0.00450,
        "Quintilla": 0.00010,
    }

    observadas = {categoria: 0 for categoria in categorias}
    for num in poker_numeros:
        categoria = _clasificar_categoria_poker(num)
        observadas[categoria] += 1

    esperadas = {categoria: n * probabilidades[categoria] for categoria in categorias}

    x = np.arange(len(categorias))
    ancho = 0.38

    plt.figure(figsize=(12, 6))
    plt.bar(
        x - ancho / 2,
        [observadas[c] for c in categorias],
        width=ancho,
        color="steelblue",
        edgecolor="black",
        label="Observadas",
    )
    plt.bar(
        x + ancho / 2,
        [esperadas[c] for c in categorias],
        width=ancho,
        color="coral",
        edgecolor="black",
        label="Esperadas",
    )

    plt.xticks(x, categorias, rotation=20)
    plt.title("Prueba de Poker: Frecuencias Observadas vs Esperadas")
    plt.xlabel("Categoria")
    plt.ylabel("Frecuencia")
    plt.grid(axis="y", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

    print("\n--- Resumen Poker ---")
    for categoria in categorias:
        print(
            f"{categoria}: O={observadas[categoria]}, "
            f"E={esperadas[categoria]:.2f}"
        )

    return {
        "observadas": observadas,
        "esperadas": esperadas,
    }


def graficar_prueba_rachas(numeros_aleatorios, alpha=0.05):
    """
    Grafica la cantidad de rachas observadas vs esperadas y muestra el
    intervalo de aceptacion asociado al nivel de confianza.

    Parameters
    ----------
    numeros_aleatorios : list[float]
        Muestra de numeros pseudoaleatorios en [0, 1).
    alpha : float, optional
        Nivel de significancia para el intervalo de confianza.

    Returns
    -------
    dict
        Resumen con rachas observadas, esperadas, intervalo y estadistico Z.
    """
    if not numeros_aleatorios:
        raise ValueError("La lista de numeros no puede estar vacia.")

    if len(numeros_aleatorios) < 2:
        raise ValueError("Se requieren al menos 2 datos para la prueba de rachas.")

    mediana_teorica = 0.5
    signos = [1 if num >= mediana_teorica else 0 for num in numeros_aleatorios]

    rachas_observadas = 1
    for i in range(1, len(signos)):
        if signos[i] != signos[i - 1]:
            rachas_observadas += 1

    n = len(numeros_aleatorios)
    n_pos = sum(signos)
    n_neg = n - n_pos
    numerador = 2 * n_pos * n_neg

    rachas_esperadas = (numerador / n) + 1
    varianza_rachas = (numerador * (numerador - n)) / ((n**2) * (n - 1))

    if varianza_rachas <= 0:
        raise ValueError(
            "No se puede calcular la prueba de rachas: varianza no positiva."
        )

    z_estadistico = (rachas_observadas - rachas_esperadas) / math.sqrt(varianza_rachas)

    z_teorico = float(norm.ppf(1 - alpha / 2))
    z_min = -z_teorico
    z_max = z_teorico

    # Transformamos el intervalo en Z a intervalo en numero de rachas.
    rachas_min = rachas_esperadas + z_min * math.sqrt(varianza_rachas)
    rachas_max = rachas_esperadas + z_max * math.sqrt(varianza_rachas)

    aceptada = z_min <= z_estadistico <= z_max

    plt.figure(figsize=(9, 6))
    etiquetas = ["Rachas Observadas", "Rachas Esperadas"]
    valores = [rachas_observadas, rachas_esperadas]

    plt.bar(etiquetas, valores, color=["steelblue", "coral"], edgecolor="black")
    plt.axhline(rachas_min, color="gray", linestyle="--", label="Limite inferior")
    plt.axhline(rachas_max, color="gray", linestyle="-.", label="Limite superior")
    plt.fill_between(
        [-0.5, 1.5],
        rachas_min,
        rachas_max,
        color="gray",
        alpha=0.15,
        label="Intervalo aceptacion",
    )

    plt.title("Prueba de Rachas: Observadas vs Esperadas")
    plt.ylabel("Cantidad de rachas")
    plt.grid(axis="y", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

    print("\n--- Resumen Rachas ---")
    print(f"Rachas observadas: {rachas_observadas}")
    print(f"Rachas esperadas: {rachas_esperadas:.4f}")
    print(f"Intervalo aceptacion: [{rachas_min:.4f}, {rachas_max:.4f}]")
    print(f"Z estadistico: {z_estadistico:.4f}")
    print(f"Resultado: {'Aceptada' if aceptada else 'Rechazada'}")

    return {
        "rachas_observadas": rachas_observadas,
        "rachas_esperadas": rachas_esperadas,
        "rachas_min": rachas_min,
        "rachas_max": rachas_max,
        "z_estadistico": z_estadistico,
        "aceptada": aceptada,
    }


__all__ = [
    "graficar_kolmogorov_smirnov",
    "graficar_prueba_poker",
    "graficar_prueba_rachas",
]
