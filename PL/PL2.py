from pulp import *
import pandas as pd

def optimize_production(initial_stock, demands, yield_percentage, density, max_productivity, safety_stocks=None):

    num_periods = len(demands)

    # Safety stock handling
    if safety_stocks is None:
        safety_stocks = [0] * num_periods  # Default to 0 if not provided
    elif len(safety_stocks) != num_periods:
        raise ValueError("Length of safety_stocks must equal the number of periods (demands).")

    # 1. Create the problem
    prob = LpProblem("Production_Optimization", LpMinimize)  # Minimize production

    # 2. Define decision variables
    production_vars = [LpVariable(f"P_{t}", 0, max_productivity) for t in range(num_periods)]  # Productivity in each period

    # 3. Define the objective function (Minimize total production)
    prob += lpSum(production_vars), "Total_Production"

    # 4. Define the constraints
    stock = initial_stock
    stocks = []
    for t in range(num_periods):
        stock = stock + (production_vars[t] * yield_percentage * density) - demands[t]
        prob += stock >= safety_stocks[t], f"Inventory_Balance_{t}"
        stocks.append(stock)

    # Final stock constraint (zero stock at the end)
    prob += stock == 0, "Final_Stock"

    # 5. Solve the problem
    prob.solve()

    # 6. Extract the results
    optimal_value = value(prob.objective)
    production_levels = [value(var) for var in production_vars]
    ending_stocks = []
    stock = initial_stock
    for t in range(num_periods):
        stock = stock + (production_levels[t] * yield_percentage * density) - demands[t]
        ending_stocks.append(stock)

    return {
        'optimal_value': optimal_value,
        'production_levels': production_levels,
        'ending_stocks': ending_stocks,
        'status': LpStatus[prob.status]
    }


if __name__ == "__main__":
    # Example usage
    initial_stock = 100
    demands = [150, 200, 180, 220]  # Quarterly demands
    yield_percentage = 0.8
    density = 0.9
    max_productivity = 300
    safety_stocks = [20, 20, 20, 0]

    try:
        results = optimize_production(initial_stock, demands, yield_percentage, density, max_productivity, safety_stocks)

        print("Optimization Results:")
        print(f"Status: {results['status']}")
        if results['status'] == 'Optimal':
            print(f"Optimal Total Production: {results['optimal_value']}")
            print("Production Levels:")
            for t, p in enumerate(results['production_levels']):
                print(f"  Quarter {t+1}: {p}")
            print("Ending Stocks:")
            for t, s in enumerate(results['ending_stocks']):
                print(f"  Quarter {t+1}: {s}")

            # Crear DataFrame para exportar
            df = pd.DataFrame({
                'Periodo': [f"Periodo {t+1}" for t in range(len(results['production_levels']))],
                'Produccion': results['production_levels'],
                'Stock_Final': results['ending_stocks'],
                'Demanda': demands,
                'Stock_Seguridad': safety_stocks
            })

            # Guardar en CSV
            df.to_csv("resultados_optimizacion.csv", index=False)
            print("\n✅ Resultados exportados a 'resultados_optimizacion.csv'")

        elif results['status'] == 'Infeasible':
            print("❌ Problema infactible: no hay solución que cumpla todas las restricciones.")
        else:
            print(f"⚠️ Estado del modelo: {results['status']}. Verifica los datos y restricciones.")
    except ValueError as e:
        print(f"Error: {e}")