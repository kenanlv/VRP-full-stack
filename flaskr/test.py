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
        # data ={'distance_matrix': [[0.0, 813.7, 787.6, 1563.2, 832.1, 63.0, 825.5, 638.5, 917.8, 778.7],
        #                      [727.7, 0.0, 237.2, 1050.1, 145.5, 692.3, 1119.9, 965.0, 327.5, 132.7],
        #                      [776.7, 216.6, 0.0, 1140.1, 293.9, 741.3, 1044.3, 811.3, 641.2, 343.6],
        #                      [1601.7, 1081.1, 1168.7, 0.0, 934.9, 1566.3, 1983.4, 1828.4, 775.5, 905.5],
        #                      [722.6, 126.0, 311.9, 864.8, 0.0, 687.2, 1411.1, 1138.9, 220.9, 59.0],
        #                      [46.8, 811.7, 785.5, 1561.2, 830.1, 0.0, 823.5, 636.4, 915.7, 776.7],
        #                      [801.6, 1087.6, 1044.5, 2196.4, 1465.3, 846.6, 0.0, 293.0, 1550.9, 1411.9],
        #                      [597.6, 921.3, 832.0, 1805.2, 1414.4, 627.4, 284.7, 0.0, 1500.1, 1361.1],
        #                      [958.9, 387.8, 455.3, 694.0, 182.2, 923.5, 1647.4, 1365.7, 0.0, 260.8],
        #                      [758.5, 175.6, 349.5, 883.4, 76.4, 723.1, 1447.0, 1174.8, 239.5, 0.0]],
        #  'capacities': [3, 4, 4, 4], 'origins': [3, 5, 6, 9], 'location': [
        #     [-122.312758, -122.3399624, -122.3603133, -122.3281019, -122.3339844, -122.3165305, -122.3570504,
        #      -122.3655963, -122.3242778, -122.3282602],
        #     [47.66395499999999, 47.6161953, 47.62273380000001, 47.5424059, 47.6081064, 47.6624768, 47.7034093,
        #      47.6823273, 47.5964476, 47.6087908]], 'time_cost': [
        #     [0.0, 13.983333333333333, 15.183333333333334, 16.866666666666667, 12.416666666666666, 3.3, 14.0,
        #      14.666666666666666, 11.4, 11.316666666666666],
        #     [12.316666666666666, 0.0, 7.216666666666667, 14.716666666666667, 7.3, 12.916666666666666,
        #      18.416666666666668, 15.7, 9.683333333333334, 7.1],
        #     [14.866666666666667, 8.116666666666667, 0.0, 15.533333333333333, 10.483333333333333, 15.45,
        #      16.683333333333334, 13.133333333333333, 12.916666666666666, 12.55],
        #     [16.8, 14.483333333333333, 17.65, 0.0, 12.166666666666666, 17.4, 24.733333333333334, 22.016666666666666,
        #      10.3, 11.416666666666666],
        #     [8.716666666666667, 6.133333333333334, 9.783333333333333, 10.533333333333333, 0.0, 9.316666666666666,
        #      16.383333333333333, 17.116666666666667, 5.016666666666667, 3.433333333333333],
        #     [2.5833333333333335, 13.716666666666667, 14.916666666666666, 16.583333333333332, 12.15, 0.0,
        #      13.733333333333333, 14.4, 11.133333333333333, 11.033333333333333],
        #     [12.333333333333334, 17.266666666666666, 16.533333333333335, 21.383333333333333, 16.933333333333334,
        #      13.866666666666667, 0.0, 6.833333333333333, 15.933333333333334, 15.833333333333334],
        #     [14.633333333333333, 14.4, 14.166666666666666, 21.166666666666668, 18.283333333333335, 16.1,
        #      5.516666666666667, 0.0, 17.266666666666666, 17.166666666666668],
        #     [12.2, 11.95, 14.916666666666666, 12.433333333333334, 7.75, 12.8, 19.866666666666667, 20.016666666666666,
        #      0.0, 6.416666666666667],
        #     [10.516666666666667, 7.716666666666667, 11.7, 11.0, 4.533333333333333, 11.116666666666667,
        #      18.183333333333334, 18.916666666666668, 5.483333333333333, 0.0]],
        #  'locations_txt': ['University of Washington, Seattle, WA, USA', '888 Western Avenue, Seattle, WA, USA',
        #                    '450 3rd Avenue West, Seattle, WA, USA', '411 University Street, Seattle, WA, USA',
        #                    '624 Yale Avenue North, Seattle, WA, USA', '4557 11th Avenue Northeast, Seattle, WA, USA',
        #                    '123 North 103rd Street, Seattle, WA, USA', '651 NW 74th St, Seattle, WA, USA',
        #                    '6705 East Marginal Way South, Seattle, WA, USA', '801 Spring Street, Seattle, WA, USA'],
        #  'email_list': ['kkenan@gs.com', 'conan.lee53@gmail.com', 'conan.lee53@gmail.com', 'conan.lee53@gmail.com',
        #                 'conan.lee53@gmail.com', 'conan.lee53@gmail.com', 'conan.lee53@gmail.com',
        #                 'conan.lee53@gmail.com', 'conan.lee53@.com', 'conan@gmail.com'],
        #  'phone_num': ['9999999999', '9999999999', '9999999999', '9999999999', '9999999999', '9999999999', '9999999999',
        #                '9999999999', '9999999999', '9999999999'],
        #  'name': ['234手动阀', '234手动阀', '234手动阀', '234手动阀', '234手动阀', '234手动阀', '234手动阀', '234手动阀', '234手动阀', '234手动阀']}

        # data = {'distance_matrix': dis_mx, 'capacities': capacities, 'origins': origins, 'location' : location}
        data = calculation_prepare()
        # print(data)
        solver = Solver(data['distance_matrix'], data['capacities'],
                        data['origins'])  # distance mx, capacities, origins
        solution = solver.solve()
        print(solution)
        locations = np.array(data['location'])
        num_locations = len(locations[0])
        num_origins = len(data['origins'])
        for i in range(num_locations):
            if i in data['origins']:
                continue
            plt.plot(locations[0, i], locations[1, i], 'kx')
        for ori in data['origins']:
            plt.plot(locations[0, ori], locations[1, ori], 'ro')
        plt.plot(locations[0][0], locations[1][0], 'bp')

        for path in solution:
            plt.plot(locations[0, path], locations[1, path])
        x_low_lim = min(data['location'][0])
        x_up_lim = max(data['location'][0])
        x_mid = (x_up_lim - x_low_lim) / 4
        y_low_lim = min(data['location'][1])
        y_up_lim = max(data['location'][1])
        y_mid = (y_up_lim - y_low_lim) / 4
        plt.xlim(x_low_lim - x_mid, x_up_lim + x_mid)
        plt.ylim(y_low_lim - y_mid, y_up_lim + y_mid)
        plt.savefig(f"templates/results/{Solver.__name__}.png", dpi=300)
        plt.clf()
        ret = {'path': solution, 'user_info': data}
        return ret
