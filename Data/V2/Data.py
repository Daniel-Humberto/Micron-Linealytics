import pandas as pd

# Cargar las hojas del archivo Excel
supply_demand = pd.read_excel("Hackaton_DB_Final.xlsx", sheet_name="Supply_Demand", skiprows=2)
boundary_conditions = pd.read_excel("Hackaton_DB_Final.xlsx", sheet_name="Boundary Conditions", skiprows=1)
yields = pd.read_excel("Hackaton_DB_Final.xlsx", sheet_name="Yield")

# Transponer los DataFrames
supply_demand = supply_demand.transpose()
boundary_conditions = boundary_conditions.transpose()
yields = yields.transpose()

# Exportar a CSV sin incluir el índice
supply_demand.to_csv("Supply_Demand.csv", index=False)
boundary_conditions.to_csv("Boundary_Conditions.csv", index=False)
yields.to_csv("Yields.csv", index=False)
