import matplotlib.pyplot as plt
import pulp

def minimize_cost(prices, arrival_time, SOC, H):
    OptimalBatteryCapacity = 60
    
    # Make a copy of electricity prices
    electricity_cost_clean = prices[:]
    
    # Adjust electricity prices for arrival and departure times
    for i in range(0, arrival_time):
        prices[i] = 120
    
    for i in range(H, 24):
        prices[i] = 120
    
    # Define the problem
    problem = pulp.LpProblem("Minimize_Electricity_Cost", pulp.LpMinimize)
    
    # Create a list of time slots
    time_slots = list(range(24))
    
    # Define the decision variables
    x = pulp.LpVariable.dicts("operation", time_slots, cat="Binary")
    
    # Objective function
    problem += pulp.lpSum([x[i] * prices[i] for i in time_slots])
    
    # Constraint: Ensure battery is fully charged by specified time
    if SOC < OptimalBatteryCapacity:
        problem += (pulp.lpSum([x[i] for i in time_slots]) == (OptimalBatteryCapacity - SOC) / 22)
    else:
        problem += pulp.lpSum([x[i] for i in time_slots]) == 0
    
    # Solve the problem
    problem.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # Extract solution
    operation_schedule = [x[i].value() for i in time_slots]
    total_cost = sum([operation_schedule[i] * prices[i] for i in time_slots])
    
    # Print total cost
    print("Total Cost:", total_cost)
    
    # Visualize results
    fig, ax1 = plt.subplots()
    color = "tab:red"
    ax1.set_xlabel("Time Slot")
    ax1.set_ylabel("Prices", color=color)
    ax1.plot(electricity_cost_clean, color=color, label="Prices")
    ax1.tick_params(axis="y", labelcolor=color)
    
    ax2 = ax1.twinx()
    color = "tab:blue"
    ax2.set_ylabel("Operation Schedule", color=color)
    ax2.plot(operation_schedule, color=color, label="Optimal Charging Schedule")
    ax2.fill_between(range(len(operation_schedule)), operation_schedule, color="blue", alpha=0.25)
    ax2.tick_params(axis="y", labelcolor=color)
    
    fig.legend(loc="upper right")
    fig.tight_layout()
    plt.show()
    
    return total_cost

# Example usage:
# prices = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 120, 120]
# arrival_time = 8
# SOC = 20
# H = 6
# minimize_cost(prices, arrival_time, SOC, H)

