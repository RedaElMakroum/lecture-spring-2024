# import matplotlib.pyplot as plt
import pulp
import copy


def minimize_cost(prices,arrival_time,SOC, H):

    OptimalBatteryCapacity= 60
    electricity_cost = prices

# Make a deep copy
    electricity_cost_clean = copy.deepcopy(prices)

# Fetch what's the usual date on which the car starts charging and what's the SOC when it starts
# This is to generate an estimation of the cycle time for that day

    # Define the problem
    problem = pulp.LpProblem("Minimize_Electricity_Cost", pulp.LpMinimize)
    # Create a list of time slots
    time_slots = list(range(24))
    # Define the decision variables
    x = pulp.LpVariable.dicts("operation", time_slots, cat='Binary')
    for i in range(0,arrival_time):
        electricity_cost[i] = 120

    for i in range(H,24):
        electricity_cost[i] = 120

    # Objective function
    problem += pulp.lpSum([x[i] * electricity_cost[i] for i in time_slots])

    # Constraint: Operation Cycle
    # problem += pulp.lpSum([x[i] for i in time_slots]) == 1.46
    
    
    
    if SOC < OptimalBatteryCapacity:
        problem += pulp.lpSum([x[i] for i in time_slots]) == (OptimalBatteryCapacity-SOC)/22
    else:
        problem += pulp.lpSum([x[i] for i in time_slots]) == 0
        
    # Constraint: After Arrival and Before 5 AM
    

    # for i in range(21):
    #     problem += x[i+3] <= x[i]  # If operation starts at hour i, it must continue for the next 3 hours
    #     problem += x[i] <= x[i+1] + 1 - x[i+3]  # If operation does not continue to hour i+3, it must stop at hour i
    problem.solve(pulp.PULP_CBC_CMD(msg=False))
    # Solve the problem
    problem.solve()

    # Extract solution
    operation_schedule = [x[i].value() for i in time_slots]
    total_cost = sum([operation_schedule[i] * electricity_cost[i] for i in time_slots])

    # print("Operation Schedule (1=operate, 0=not operate):", operation_schedule)
    print("Cost:", total_cost)

    # fig, ax1 = plt.subplots()

    # color = 'tab:red'
    # ax1.set_xlabel('Time Slot')
    # ax1.set_ylabel('Prices', color=color)
    # ax1.plot(electricity_cost_clean, color=color)
    # ax1.tick_params(axis='y', labelcolor=color)
    # ax1.plot(electricity_cost_clean, color=color, label='Prices')


    # ax2 = ax1.twinx()  
    # color = 'tab:blue'
    # ax2.set_ylabel('Operation Schedule', color=color)  
    # ax2.plot(operation_schedule, color=color)
    # ax2.tick_params(axis='y', labelcolor=color)
    # ax2.plot(operation_schedule, color=color, label='Optimal Charging Schedule')
    # ax2.fill_between(range(len(operation_schedule)), operation_schedule, color='blue', alpha=0.25)

    # fig.legend(loc="upper right")

    # fig.tight_layout()  
    # plt.show()


    return total_cost

# Call the function with the prices
# minimize_cost(helper.prices)


