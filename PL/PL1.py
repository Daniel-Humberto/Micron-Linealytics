from pulp import *

def optimize_production(initial_stock, demands, yield_percentage, density, max_productivity, safety_stocks=None):
    """
    Optimizes production plan using linear programming to meet demand while minimizing productivity,
    considering yield, density, safety stock, and a final target stock of zero.

    Args:
        initial_stock (float): The initial stock level.
        demands (list of float): The demand for each period.
        yield_percentage (float): The yield percentage (0 to 1).
        density (float): The production density factor.
        max_productivity (float): The maximum productivity per period.
        safety_stocks (list of float, optional): The safety stock for each period.
            If None, no safety stock constraint is applied.  Defaults to None.
            Must be the same length as demands if provided.

    Returns:
        dict: A dictionary containing the optimal solution:
            - 'optimal_value': The optimal total productivity.
            - 'production_levels': A list of optimal production levels for each period.
            - 'ending_stocks': A list of ending stock levels for each period.
            - 'status': The status of the optimization ('Optimal', 'Infeasible', etc.)
    """
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

if __name__ == "__main__":
    # Example usage
    initial_stock = 100
    demands = [150, 200, 180, 220]  # Quarterly demands
    yield_percentage = 0.8  # 80% yield
    density = 0.9      # 90% density
    max_productivity = 300
    safety_stocks = [20, 20, 20, 0] # Example safety stock levels.  Last one is 0.

    try:
        results = optimize_production(initial_stock, demands, yield_percentage, density, max_productivity, safety_stocks)

        print("Optimization Results:")
        print(f"Status: {results['status']}")  # Print the status
        if results['status'] == 'Optimal':
            print(f"Optimal Total Production: {results['optimal_value']}")
            print("Production Levels:")
            for t, p in enumerate(results['production_levels']):
                print(f"  Quarter {t+1}: {p}")
            print("Ending Stocks:")
            for t, s in enumerate(results['ending_stocks']):
                print(f"  Quarter {t+1}: {s}")
        elif results['status'] == 'Infeasible':
            print("Problem is infeasible: No solution satisfies all constraints.")
        else:
            print(f"Problem status: {results['status']}.  Check the model and data.")
    except ValueError as e:
        print(f"Error: {e}")