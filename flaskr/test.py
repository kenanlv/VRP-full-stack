from templates.solver_google import GoogleLocalSearchSolver
from routing_calculation_init import calculation_prepare


def solving_for_route():
    data = calculation_prepare()
    solver = GoogleLocalSearchSolver(data['distance_matrix'], data['capacities'],
                                     data['origins'])  # distance mx, capacities, origins
    solution = solver.solve()
    print(solution)
    ret = {'path': solution, 'user_info': data}
    return ret
