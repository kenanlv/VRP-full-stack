from templates.solver_google import GoogleLocalSearchSolver, GoogleFirstSolutionSolver
from templates.solver_notGoogle import SolverNotGoogle
import json
import matplotlib.pyplot as plt
import numpy as np
from os import listdir
from routing_calculation_init import calculation_prepare


def solving_for_route():
    # Solvers = [GoogleLocalSearchSolver, GoogleFirstSolutionSolver, SolverNotGoogle]
    Solvers = [GoogleLocalSearchSolver]
    for Solver in Solvers:
        data = calculation_prepare()
        # print(data)
        solver = Solver(data['distance_matrix'], data['capacities'],
                        data['origins'])  # distance mx, capacities, origins
        solution = solver.solve()
        print(solution)
        # locations = np.array(data['location'])
        # num_locations = len(locations[0])
        # num_origins = len(data['origins'])
        # for i in range(num_locations):
        #     if i in data['origins']:
        #         continue
        #     plt.plot(locations[0, i], locations[1, i], 'kx')
        # for ori in data['origins']:
        #     plt.plot(locations[0, ori], locations[1, ori], 'ro')
        # plt.plot(locations[0][0], locations[1][0], 'bp')
        #
        # for path in solution:
        #     plt.plot(locations[0, path], locations[1, path])
        # x_low_lim = min(data['location'][0])
        # x_up_lim = max(data['location'][0])
        # x_mid = (x_up_lim - x_low_lim) / 4
        # y_low_lim = min(data['location'][1])
        # y_up_lim = max(data['location'][1])
        # y_mid = (y_up_lim - y_low_lim) / 4
        # plt.xlim(x_low_lim - x_mid, x_up_lim + x_mid)
        # plt.ylim(y_low_lim - y_mid, y_up_lim + y_mid)
        # plt.savefig(f"templates/results/{Solver.__name__}.png", dpi=300)
        # plt.clf()
        ret = {'path': solution, 'user_info': data}
        return ret
