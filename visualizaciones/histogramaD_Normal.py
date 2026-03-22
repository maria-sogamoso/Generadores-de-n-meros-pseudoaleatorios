import matplotlib.pyplot as plt
from distribuciones.normal import GeneradorDistribucionNormal
from generador_numeros.congruencia_lineal import GeneradorCongruenciaLineal


def _graficar_histogramas(numeros, titulo, bins=50):
	"""
	Dibuja dos histogramas de la misma secuencia:
	1. Escala normal
	2. Escala logaritmica

	Parameters
	----------
	numeros : list[float]
		Secuencia de valores de la distribucion normal.
	titulo : str
		Titulo general de la figura.
	bins : int, optional
		Numero de intervalos del histograma.
	"""
	fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

	ax1.hist(
		numeros,
		bins=bins,
		color="steelblue",
		edgecolor="black",
		alpha=0.75
	)
	ax1.set_title("Vista Normal")
	ax1.set_xlabel("Valor")
	ax1.set_ylabel("Frecuencia")
	ax1.grid(axis="y", alpha=0.3)

	ax2.hist(
		numeros,
		bins=bins,
		color="coral",
		edgecolor="black",
		alpha=0.75
	)
	ax2.set_title("Escala Logaritmica")
	ax2.set_xlabel("Valor")
	ax2.set_ylabel("Frecuencia (log)")
	ax2.set_yscale("log")
	ax2.grid(axis="y", alpha=0.3, which="both")

	plt.suptitle(titulo, fontsize=12, fontweight="bold")
	plt.tight_layout()
	plt.show()


def visualizar_histograma_distribucion_normal(
	semilla,
	pasos,
	mu=0.0,
	sigma=1.0,
	bins=50,
):
	"""
	Genera una muestra con distribucion normal N(mu, sigma^2)
	y muestra su distribucion en histogramas.

	Flujo de generacion:
		1) Generar base uniforme con Congruencia Lineal.
		2) Transformar con Box-Muller a distribucion normal.

	Parameters
	----------
	semilla : int
		Semilla para el generador congruencial lineal.
	pasos : int
		Cantidad de valores normales solicitados.
	mu : float, optional
		Media objetivo de la normal.
	sigma : float, optional
		Desviacion estandar objetivo de la normal.
	bins : int, optional
		Numero de intervalos para los histogramas.
	"""
	gen_base = GeneradorCongruenciaLineal(semilla=semilla)
	uniformes_base = gen_base.siguiente_Ri_Congruencia_Lineal(pasos)

	# Box-Muller requiere valores estrictamente en (0, 1).
	epsilon = 1e-12
	uniformes_ajustados = [
		min(max(u, epsilon), 1.0 - epsilon) for u in uniformes_base
	]

	gen_normal = GeneradorDistribucionNormal(mu=mu, sigma=sigma)
	numeros = gen_normal.generar(uniformes_ajustados)[:pasos]

	titulo = (
		"Histograma de Frecuencia - Distribucion Normal\n"
		f"Semilla: {semilla}, mu: {mu}, sigma: {sigma}, Muestras: {pasos}"
	)

	print("\n--- Estadisticas ---")
	print(f"Total de numeros: {len(numeros)}")
	print(f'Lista de numeros: {numeros[:10]}{"..." if len(numeros) > 10 else ""}')
	print(f"Minimo: {min(numeros):.8f}")
	print(f"Maximo: {max(numeros):.8f}")
	print(f"Media: {sum(numeros)/len(numeros):.8f}")
	print(f"Esperado (normal): mu = {mu}")

	_graficar_histogramas(numeros, titulo, bins=bins)
