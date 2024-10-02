import matplotlib.pyplot as plt
import pandas as pd

datos = pd.read_csv('Resultados_tiempo.csv')
print(datos.columns)
datos.columns = datos.columns.str.strip()

plt.figure(figsize=(12, 6))
plt.errorbar(datos['Numero de Claves'], datos['Comparaciones Promedio'], yerr=datos['Desviacion Estandar'],
             marker='o', linestyle='-', color='b', ecolor='r', elinewidth=1, capsize=3, label='Comparaciones promedio')

fig, ax1 = plt.subplots(figsize=(12, 6))

color = 'tab:blue'
ax1.set_xlabel('Número de claves')
ax1.set_ylabel('Comparaciones promedio', color=color)
ax1.errorbar(datos['Numero de Claves'], datos['Comparaciones Promedio'], yerr=datos['Desviacion Estandar'],
             marker='o', linestyle='-', color=color, ecolor='r', elinewidth=1, capsize=3, label='Comparaciones promedio')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  
color = 'tab:green'
ax2.set_ylabel('Tiempo promedio (ns)', color=color)
ax2.plot(datos['Numero de Claves'], datos['Tiempo Promedio (ns)'], marker='s', linestyle='--', color=color, label='Tiempo promedio')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Comparaciones promedio y Tiempo promedio vs Número de claves en Red-Black Tree')
fig.tight_layout()
plt.grid(True)
plt.savefig('grafico_comparaciones_y_tiempo.png')
plt.show()
