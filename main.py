from gurobipy import GRB, Model, quicksum
from process_data import *

model = Model()
model.setParam('TimeLimit',1800)

M = range(1, 5 + 1) #Materiales
I = range(1, 7 + 1) #Regiones
D = range(1, 3 + 1) #Dimensiones
T = range(1, 50 + 1) #Años
T_2 = range(0, 50 + 1)
N = 999999999  #Big 'M' 


# Definición de parámetros a partir de data

demanda = {(i, t): demanda_anual()[i,t] for i in I for t in T} 
costo_m = {(m, i, d, t): costo_mantencion()[m,i ,d, t] for m in M for i in I for d in D for t in T}
costo_i = {(m, i, d, t): costo_instalacion()[m,i,d,t] for m in M for i in I for d in D for t in T}
capacidad_max ={(m, i, d): capacidad_maxima()[m,i,d] for m in M for i in I for d in D}
humedad = {(i, t): humedad_anual()[i,t] for i in I for t in T}
eficiencia = {m: eficiencia_material()[m] for m in M}
superficie = {i: superficie_efectiva()[i] for i in I}
area = {d: area_ocupada()[d] for d in D}
per = {i: plazo_mantenimiento()[i] for i in I}
gamma = {(m, i, d): 584000 for m in M for i in I for d in D}

# Variables

x = model.addVars(M, I, D, T_2, vtype = GRB.INTEGER, name = "x_midt")
y = model.addVars(M, I, D, T, vtype = GRB.INTEGER, name = "y_midt")
w = model.addVars(I, T, vtype = GRB.CONTINUOUS, name = "w_it") 
z = model.addVars(M, I, D, T, vtype = GRB.BINARY, name = "z_midt") 
q = model.addVars(M, I, D, T, vtype = GRB.BINARY, name = "q_midt") 

# Restricciones

model.addConstrs((w[i, t - 1] + quicksum(eficiencia[m] * humedad[i, t] * capacidad_max[m, i, d] * x[m, i, d, t] for d in D for m in M) == demanda[i, t] + w[i, t] for i in I for t in range(2, 51)), name = "R1.1")

model.addConstrs((x[m,i,d,t] <= x[m,i,d,t+1] for m in M for i in I for d in D for t in range(1,50)), name= 'r_bonus')

model.addConstrs(x[m,i,d, 0] == 0 for m in M for i in I for d in D)

model.addConstrs((quicksum(eficiencia[m] * humedad[i, 1] * capacidad_max[m, i, d] * x[m, i, d, 1] for d in D for m in M) == demanda[i, 1] + w[i, 1] for i in I), name = "R1.2")

model.addConstrs((y[m, i, d, t] <= N * q[m, i, d, t] for m in M for i in I for t in T for d in D), name = "R3.1")

model.addConstrs((y[m, i, d, t] <= x[m, i, d, t] for i in I for m in M for d in D for t in T), name = "R3.3")

model.addConstrs((y[m, i, d, t] >= x[m, i, d, t] - N * (1 - q[m, i, d, t]) for i in I for m in M for d in D for t in T), name = "R3.4")

model.addConstrs((gamma[m, i, d] + z[m, i, d, t] * N >= quicksum(eficiencia[m] * humedad[i, r] * capacidad_max[m, i, d] * x[m, i, d, r] for r in range(max(3, t), min(51, t + s + 1))) for i in I for m in M for d in D for t in range(3, 51) for s in range(2, max(2, per[i]))), name="R4.1")

model.addConstrs((z[m, i, d, t] <= q[m, i, d, t] for i in I for m in M for d in D for t in T), name = "R5")

model.addConstrs((quicksum(q[m, i, d, t - per[i] + j] for j in range(3, per[i] + 1)) >= 1 for m in M for i in I for d in D for t in range(max(3, per[i]), 51)), name="R6.1")

model.addConstrs((quicksum(area[d] * x[m, i, d, t] for m in M for d in D) <= superficie[i] for i in I for t in T), name = "R8")

# Agregar restricciones al modelo

model.update()

funcion_objetivo = quicksum(costo_m[m, i ,d , t_1] * y[m, i, d, t_1] + costo_i[m , i, d, t_1] * (x[m, i , d , t] - x[m, i, d, t - 1]) for m in M for i in I for d in D for t_1 in T for t in range(1,51))

model.setObjective(funcion_objetivo, GRB.MINIMIZE) # Colocar la FO m.optimize()

# Optimizar

model.optimize()


print(f"El valor minimo en UF para la realizacion del proyecto es: {model.ObjVal}")


# Guardar archivos y definir para gráficos 

valor_objetivo = model.ObjVal

dict_m = {
    1: "Rachel 35%",
    2: "Rachel 50%",
    3: "Tela quirurgica",
    4: "Costal de fique",
    5: "Guata"}

dict_d = {
    1: 48,
    2: 100,
    3: 150}

dict_i = {
    1: "Atacama",
    2: "Coquimbo",
    3: "Valparaiso",
    4: "Metropolitana",
    5: "Ohiggins",
    6: "Maule",
    7: "Nuble"}
print("")


demanda = demanta_total()
precio_peso = (model.ObjVal / demanda)* 36081

atrapanieblas_region = []
agua_almacenada = []
atrapanieblas_mantenidos = []
atrapanieblas_material = []
atrapanieblas_dimension = []

totales = 0
for i in I:
    cantidad = sum(x[m,i,d,50].x for m in M for d in D)
    totales += cantidad


for i in I:
    cantidad = sum(x[m,i,d,50].x for m in M for d in D)
    region = dict_i[i]
    fila = [region, int(cantidad)]
    atrapanieblas_region.append(fila)

for t in T:
    cantidad = sum(w[i, t].x for i in I)
    año = t 
    fila = [año + 2024 , int(cantidad)]
    agua_almacenada.append(fila)

for t in T:
    cantidad_mantenida = sum(y[m,i,d,t].x for m in M for i in I for d in D)
    año = t
    fila = [año + 2024, int(cantidad_mantenida)]
    atrapanieblas_mantenidos.append(fila)

for i in I:
    for m in M:
        cantidad = sum(x[m,i,d,50].x for d in D)
        region = dict_i[i]
        fila = [region, dict_m[m], int(cantidad)]
        atrapanieblas_material.append(fila)

for i in I:
    for d in D:
        cantidad = sum(x[m,i,d,50].x for m in M)
        region = dict_i[i]
        fila = [region, dict_d[d], int(cantidad)]
        atrapanieblas_dimension.append(fila)


with open('resultados_especificos/w[i,t].txt', 'w') as archivo:
    for i in I:
        for t in T:
            if w[i, t].x != 0:
                archivo.write(f"Se almacenan {int(w[i, t].x)} litros de agua en la region de {dict_i[i]} en {t + 2024} \n")
                archivo.write("")

with open('resultados_especificos/x[m,i,d,t].txt', 'w') as archivo:
    for i in I:
        for t in T:
            for d in D:
                for m in M:
                    if x[m, i, d, t].x != 0:
                        archivo.write(f"Existen {int(x[m, i, d, t].x)} atrapanieblas de material {dict_m[m]} y dimension {dict_d[d]} m^2, en la region de {dict_i[i]} a finales de {t + 2024}\n")
                        archivo.write("")

with open('resultados_especificos/y[m,i,d,t].txt', 'w') as archivo:
    for i in I:
        for t in T:
            for d in D:
                for m in M:
                    if y[m, i, d, t].x != 0:
                        archivo.write(f"{int(y[m, i, d, t].x)} atrapanieblas de material {dict_m[m]} y dimension {dict_d[d]} m^2, en la region de {dict_i[i]} reciben mantencion en {t + 2024}\n")
                        archivo.write("")

with open('resultados_especificos/z[m,i,d,t].txt', 'w') as archivo:
    for i in I:
        for t in T:
            for d in D:
                for m in M:
                    if z[m, i, d, t].x != 0:
                        archivo.write(f"{int(z[m, i, d, t].x)} atrapanieblas de material {dict_m[m]} y dimension {dict_d[d]} m^2, en la region de {dict_i[i]} superan límite de obtención en {t + 2024}\n")
                        archivo.write("")

with open('resultados_especificos/q[m,i,d,t].txt', 'w') as archivo:
    for i in I:
        for t in T:
            for d in D:
                for m in M:
                    if q[m, i, d, t].x != 0:
                        archivo.write(f"Se debe hacer mantencion a los atrapanieblas de material {dict_m[m]} y dimension {dict_d[d]} m^2, en la region de {dict_i[i]} en {t + 2024}\n")
                        archivo.write("")


 
