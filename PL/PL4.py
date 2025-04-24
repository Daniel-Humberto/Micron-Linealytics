from pulp import *
import matplotlib.pyplot as plt

def optimize_production(initial_stock, demands, yield_percentage, density, max_productivity, safety_stocks=None, objective='minimize'):
    """
    Optimizes the production plan using linear programming to meet demand, either minimizing or
    maximizing productivity, considering yield, density, safety stock, and a final target stock of zero.

    Args:
        initial_stock (float): The initial stock level.
        demands (list of float): The demand for each period.
        yield_percentage (float): The yield percentage (0 to 1).
        density (float): The production density factor.
        max_productivity (float): The maximum productivity per period.
        safety_stocks (list of float, optional): The safety stock for each period.
            If None, no safety stock constraint is applied. Defaults to None.
            Must be the same length as demands if provided.
        objective (str, optional): The optimization objective. Can be 'minimize' or 'maximize'.
            Defaults to 'minimize'.

    Returns:
        dict: A dictionary containing the optimal solution:
            - 'optimal_value': The optimal total productivity.
            - 'production_levels': A list of optimal production levels for each period.
            - 'ending_stocks': A list of ending stock levels for each period.
            - 'status': The status of the optimization ('Optimal', 'Infeasible', etc.).
    """
    num_periods = len(demands)

    # Safety stock handling
    if safety_stocks is None:
        safety_stocks = [0] * num_periods  # Default to 0 if not provided
    elif len(safety_stocks) != num_periods:
        raise ValueError("Length of safety_stocks must equal the number of periods (demands).")

    # 1. Create the problem
    if objective.lower() == 'minimize':
        prob = LpProblem("Production_Optimization_Minimize", LpMinimize)
    elif objective.lower() == 'maximize':
        prob = LpProblem("Production_Optimization_Maximize", LpMaximize)
    else:
        raise ValueError("Invalid objective. Choose 'minimize' or 'maximize'.")

    # 2. Define decision variables
    production_vars = [LpVariable(f"P_{t}", 0, max_productivity) for t in range(num_periods)]  # Productivity in each period

    # 3. Define the objective function (Minimize or Maximize total production)
    prob += lpSum(production_vars), "Total_Production"

    # 4. Define the constraints
    stock = initial_stock
    for t in range(num_periods):
        # Inventory balance constraint
        stock = stock + (production_vars[t] * yield_percentage * density) - demands[t]
        prob += stock >= safety_stocks[t], f"Inventory_Balance_{t}"

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
        'status': LpStatus[prob.status]  # Get the status string
    }

def visualize_results(results, demands):
    """
    Generates relevant plots to visualize the production optimization results.

    Args:
        results (dict): The dictionary containing the optimization results.
        demands (list of float): The demand for each period.
    """
    num_periods = len(demands)
    periods = range(1, num_periods + 1)

    if results['status'] == 'Optimal':
        # Plot Production Levels
        plt.figure(figsize=(10, 6))
        plt.plot(periods, results['production_levels'], marker='o', label='Production Level')
        plt.xlabel("Period")
        plt.ylabel("Production Quantity")
        plt.title("Optimal Production Levels per Period")
        plt.xticks(periods)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

        # Plot Ending Stock Levels and Safety Stocks
        plt.figure(figsize=(10, 6))
        plt.plot(periods, results['ending_stocks'], marker='o', label='Ending Stock Level')
        if 'safety_stocks' in locals() and safety_stocks is not None:
            plt.plot(periods, safety_stocks, linestyle='--', label='Safety Stock Level')
        plt.axhline(0, color='r', linestyle='--', label='Target Final Stock (0)')
        plt.xlabel("Period")
        plt.ylabel("Stock Level")
        plt.title("Ending Stock Levels per Period")
        plt.xticks(periods)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

        # Plot Demand vs. Production
        plt.figure(figsize=(10, 6))
        plt.bar(periods, demands, label='Demand', alpha=0.6)
        plt.plot(periods, results['production_levels'], marker='o', linestyle='-', color='green', label='Production Level')
        plt.xlabel("Period")
        plt.ylabel("Quantity")
        plt.title("Demand vs. Optimal Production Levels per Period")
        plt.xticks(periods)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    else:
        print("No visualization available as the problem is not optimal.")

if __name__ == "__main__":
    # Example usage
    initial_stock = 100
    demands = [150, 200, 180, 220]  # Quarterly demands
    yield_percentage = 0.8  # 80% yield
    density = 0.9      # 90% density
    max_productivity = 300
    safety_stocks = [20, 20, 20, 0] # Example safety stock levels. Last one is 0.

    # Optimize to minimize productivity
    try:
        results_min = optimize_production(initial_stock, demands, yield_percentage, density, max_productivity, safety_stocks, objective='minimize')

        print("\n--- Optimization Results (Minimize Productivity) ---")
        print(f"Status: {results_min['status']}")
        if results_min['status'] == 'Optimal':
            print(f"Optimal Total Production: {results_min['optimal_value']}")
            print("Production Levels:")
            for t, p in enumerate(results_min['production_levels']):
                print(f"  Period {t+1}: {p}")
            print("Ending Stocks:")
            for t, s in enumerate(results_min['ending_stocks']):
                print(f"  Period {t+1}: {s}")
            visualize_results(results_min, demands)
        elif results_min['status'] == 'Infeasible':
            print("Problem is infeasible: No solution satisfies all constraints.")
        else:
            print(f"Problem status: {results_min['status']}. Check the model and data.")
    except ValueError as e:
        print(f"Error: {e}")

    # Optimize to maximize productivity
    try:
        results_max = optimize_production(initial_stock, demands, yield_percentage, density, max_productivity, safety_stocks, objective='maximize')

        print("\n--- Optimization Results (Maximize Productivity) ---")
        print(f"Status: {results_max['status']}")
        if results_max['status'] == 'Optimal':
            print(f"Optimal Total Production: {results_max['optimal_value']}")
            print("Production Levels:")
            for t, p in enumerate(results_max['production_levels']):
                print(f"  Period {t+1}: {p}")
            print("Ending Stocks:")
            for t, s in enumerate(results_max['ending_stocks']):
                print(f"  Period {t+1}: {s}")
            visualize_results(results_max, demands)
        elif results_max['status'] == 'Infeasible':
            print("Problem is infeasible: No solution satisfies all constraints.")
        else:
            print(f"Problem status: {results_max['status']}. Check the model and data.")
    except ValueError as e:
        print(f"Error: {e}")