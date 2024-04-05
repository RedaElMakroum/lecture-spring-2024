from EVSchedule import minimize_cost

arrival_time = 0
prices = [
    50.23,
    48.67,
    46.55,
    45.00,
    43.89,
    45.25,
    47.60,
    50.20,
    55.30,
    60.00,
    62.75,
    65.00,
    68.20,
    70.00,
    72.30,
    74.50,
    76.80,
    78.00,
    77.25,
    75.00,
    73.50,
    70.40,
    68.20,
    66.00,
]
H = 14


def test_minimize_cost():
    result = minimize_cost(prices, arrival_time, 0, H)
    assert isinstance(result, (int, float))
    assert result > 0
