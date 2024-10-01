import matplotlib.pyplot as plt
import pandas as pd

# Cargar los resultados desde el archivo CSV
datos = pd.read_csv('Resultados.csv')
print(datos.columns)
datos.columns = datos.columns.str.strip()

# Graficar el número de claves vs comparaciones promedio
plt.figure(figsize=(10, 6))
plt.plot(datos['Numero de Claves'], datos['Comparaciones Promedio'], marker='o', linestyle='-', color='b', label='Comparaciones promedio')
plt.xlabel('Número de claves')
plt.ylabel('Comparaciones promedio')
plt.title('Comparaciones promedio vs Número de claves en Red-Black Tree')
plt.legend()
plt.grid(True)
plt.savefig('grafico_comparaciones.png')  # Guarda el gráfico como un archivo de imagen
plt.show()