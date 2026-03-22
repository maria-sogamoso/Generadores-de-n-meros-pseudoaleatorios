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



__all__ = [
	"graficar_kolmogorov_smirnov",
]
