import pandas as pd
import numpy as np




Supply_Demand = pd.read_excel("Hackaton_DB_Final.xlsx", sheet_name="Supply_Demand",skiprows=2)

Boundary_Conditions = pd.read_excel("Hackaton_DB_Final.xlsx", sheet_name="Boundary Conditions")


# Transpose the DataFrame
Supply_Demand = Supply_Demand.transpose()
Supply_Demand


Boundary_Conditions = pd.read_excel("Hackaton_DB_Final.xlsx", sheet_name="Boundary Conditions",skiprows=1)

Boundary_Conditions= Boundary_Conditions.transpose()
Boundary_Conditions


Yields = pd.read_excel("Hackaton_DB_Final.xlsx", sheet_name="Yield")
Yields = Yields.transpose()
Yields


Supply_Demand.to_csv("Supply_Demand.csv", index=False)
Boundary_Conditions.to_csv("Boundary_Conditions.csv", index=False)
Yields.to_csv("Yields.csv", index=False)