import pandas as pd
import numpy as np

# Cargar datos desde el Excel
Supply_Demand = pd.read_excel("Hackaton_DB_Final.xlsx", sheet_name="Supply_Demand", skiprows=2)
Boundary_Conditions = pd.read_excel("Hackaton_DB_Final.xlsx", sheet_name="Boundary Conditions", skiprows=1)
Yields = pd.read_excel("Hackaton_DB_Final.xlsx", sheet_name="Yield")

# Transponer los DataFrames
Supply_Demand = Supply_Demand.transpose()
Boundary_Conditions = Boundary_Conditions.transpose()
Yields = Yields.transpose()

# Resetear índice de Supply_Demand por claridad
Supply_Demand.reset_index(drop=True, inplace=True)

# Granular filas a partir de la fila 4 (índice 3), considerando 13 semanas
def granular_semanal(df, semanas=13, fila_inicio=3):
    filas_granuladas = []

    for i in range(len(df)):
        fila_original = df.iloc[i]

        if i < fila_inicio:
            # No granular las filas iniciales
            filas_granuladas.append(fila_original)
        else:
            # Repetir la fila 13 veces (una por cada semana)
            for semana in range(1, semanas + 1):
                nueva_fila = fila_original.copy()
                nueva_fila["Semana"] = semana
                filas_granuladas.append(nueva_fila)

    return pd.DataFrame(filas_granuladas)

# Aplicar granularización a Supply_Demand
Supply_Demand_granulado = granular_semanal(Supply_Demand)

# Exportar los resultados a CSV
Supply_Demand_granulado.to_csv("Supply_Demand.csv", index=False)
Boundary_Conditions.to_csv("Boundary_Conditions.csv", index=False)
Yields.to_csv("Yields.csv", index=False)