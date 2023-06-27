#Al ejecutar esto ejecuta el modelo y cambia los valores de resultados_generales.txt con lo principal.
#Requiere instalar la librería tabulate (sirve para escribir tablas solamente) (pip install tabulate en cmd)
#Abrirá los gráficos para observación y actualizará resultados.txt

import pandas as pd 
import matplotlib.pyplot as plt
from main import atrapanieblas_region, agua_almacenada, valor_objetivo,atrapanieblas_mantenidos, atrapanieblas_dimension, atrapanieblas_material, precio_peso,totales
from tabulate import tabulate

data_atrapanieblas = pd.DataFrame(atrapanieblas_region, columns = ['Región','Atrapanieblas'])
plt.bar(data_atrapanieblas['Región'], data_atrapanieblas['Atrapanieblas'])
plt.title('Cantidad de atrapanieblas al término del proyecto')
plt.xlabel('Regiones')
plt.ylabel('Cantidad de atrapanieblas')
plt.show()

data_agua = pd.DataFrame(agua_almacenada, columns = ['Año','Agua almacenada'])
plt.plot(data_agua['Año'], data_agua['Agua almacenada'])
plt.title('Cantidad de agua almacenada')
plt.xlabel('Año')
plt.ylabel('Cantidad de agua almacenada')
plt.show()

data_mantenidos = pd.DataFrame(atrapanieblas_mantenidos, columns = ['Año', 'Atrapanieblas mantenidos'])
plt.plot(data_mantenidos['Año'], data_mantenidos['Atrapanieblas mantenidos'])
plt.title('Cantidad de atrapanieblas mantenidos')
plt.xlabel('Año')
plt.ylabel('Cantidad de atrapanieblas')
plt.show()

tabla_region = tabulate(atrapanieblas_region, headers=["Region", "Cantidad de Atrapanieblas"])
tabla_region += "\n"

tabla_agua = tabulate(agua_almacenada, headers=["Ano", "Cantidad de Agua Almacenada"])
tabla_agua += "\n"

tabla_material = tabulate(atrapanieblas_material, headers=['Region',"Material", "Cantidad de Atrapanieblas"])
tabla_material += "\n"

tabla_dimension = tabulate(atrapanieblas_dimension, headers=['Region',"Dimension", "Cantidad de Atrapanieblas"])
tabla_dimension += "\n"

with open("resultados_generales.txt", "w") as archivo:
    
    archivo.write(f'El proyecto gasta {valor_objetivo} UF, equivalente {valor_objetivo * 36081} pesos chilenos en todo el proyecto \n')
    archivo.write(f'Lo anterior es equivalente a {valor_objetivo * 36081 / 50} pesos anual y {valor_objetivo * 36081 / (50 * 7)} por region en promedio anual\n')
    archivo.write("\n")


    archivo.write(f'El precio por litro de agua en nuestro proyecto es de {precio_peso}\n')
    archivo.write("\n")


    archivo.write(f'Se instalaron un total de {int(totales)} atrapanieblas durante el proyecto\n')
    archivo.write("\n")



    archivo.write("Tabla de Regiones y cantidad de Atrapanieblas:\n")
    archivo.write("\n")
    archivo.write(tabla_region)
    archivo.write("\n")

    archivo.write("Tabla de Anos y Cantidad de Agua Almacenada:\n")
    archivo.write("\n")
    archivo.write(tabla_agua)
    archivo.write("\n")

    archivo.write("Tabla de Materiales y Cantidad de Atrapanieblas:\n")
    archivo.write("\n")
    archivo.write(tabla_material)
    archivo.write("\n")

    archivo.write("Tabla de Dimensiones y Cantidad de Atrapanieblas:\n")
    archivo.write("\n")
    archivo.write(tabla_dimension)
    archivo.write("\n")

print("Las tablas se han guardado en el archivo resultados.txt.")