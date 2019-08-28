from .solver import BaseSolver
from typing import List
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


class GoogleLocalSearchSolver(BaseSolver):
    def solve(self) -> List[List[int]]:
        def print_solution(manager, routing, assignment):
            """Prints assignment on console."""
            total_distance = 0
            total_load = 0
            result = []
            for vehicle_id in range(len(self.capacities)):
                temp = []
                index = routing.Start(vehicle_id)
                plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
                route_distance = 0
                route_load = 0
                while not routing.IsEnd(index):
                    node_index = manager.IndexToNode(index)
                    route_load += 0 if node_index <= len(self.origins) else 1
                    temp.append(node_index)
                    plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
                    previous_index = index
                    index = assignment.Value(routing.NextVar(index))
                    distance = routing.GetArcCostForVehicle(
                        previous_index, index, vehicle_id)
                    route_distance += distance
                    plan_output += ' {0}m -> '.format(distance)
                temp.append(manager.IndexToNode(index))
                result.append(temp)
                plan_output += ' {0} Load({1})\n'.format(
                    manager.IndexToNode(index), route_load)
                plan_output += 'Distance of the route: {}m\n'.format(route_distance)
                plan_output += 'Load of the route: {}\n'.format(route_load)
                print(plan_output)
                total_distance += route_distance
                total_load += route_load
            print('Total distance of all routes: {}m'.format(total_distance))
            print('Total load of all routes: {}'.format(total_load))
            return result

        manager = pywrapcp.RoutingIndexManager(
            self.num_locations, len(self.capacities), self.origins, [self.destination] * len(self.capacities)
        )
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return self.distance_matrix[from_node][to_node] * 100

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        routing.AddDimension(
            transit_callback_index,
            0,
            300000,
            True,
            'Distance'
        )

        def demand_callback(from_index):
            return 0 if manager.IndexToNode(from_index) in self.origins else 1

        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,
            self.capacities,
            True,
            'Capacity'
        )

        distance_dimension = routing.GetDimensionOrDie('Distance')
        distance_dimension.SetGlobalSpanCostCoefficient(10000)

        search_parameter = pywrapcp.DefaultRoutingSearchParameters()
        # search_parameter.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
        search_parameter.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        search_parameter.time_limit.seconds = 15

        assignment = routing.SolveWithParameters(search_parameter)

        if assignment:
            return print_solution(manager, routing, assignment)


class GoogleFirstSolutionSolver(BaseSolver):
    def solve(self) -> List[List[int]]:
        def print_solution(manager, routing, assignment):
            """Prints assignment on console."""
            total_distance = 0
            total_load = 0
            result = []
            for vehicle_id in range(len(self.capacities)):
                temp = []
                index = routing.Start(vehicle_id)
                plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
                route_distance = 0
                route_load = 0
                while not routing.IsEnd(index):
                    node_index = manager.IndexToNode(index)
                    route_load += 0 if node_index <= len(self.origins) else 1
                    temp.append(node_index)
                    plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
                    previous_index = index
                    index = assignment.Value(routing.NextVar(index))
                    distance = routing.GetArcCostForVehicle(
                        previous_index, index, vehicle_id)
                    route_distance += distance
                    plan_output += ' {0}m -> '.format(distance)
                temp.append(manager.IndexToNode(index))
                result.append(temp)
                plan_output += ' {0} Load({1})\n'.format(
                    manager.IndexToNode(index), route_load)
                plan_output += 'Distance of the route: {}m\n'.format(route_distance)
                plan_output += 'Load of the route: {}\n'.format(route_load)
                print(plan_output)
                total_distance += route_distance
                total_load += route_load
            print('Total distance of all routes: {}m'.format(total_distance))
            print('Total load of all routes: {}'.format(total_load))
            return result

        manager = pywrapcp.RoutingIndexManager(
            self.num_locations, len(self.capacities), self.origins, [self.destination] * len(self.capacities)
        )
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return self.distance_matrix[from_node][to_node]  # Change from *100 to Nothing

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        routing.AddDimension(
            transit_callback_index,
            0,
            300000,
            True,
            'Distance'
        )

        def demand_callback(from_index):
            return 0 if manager.IndexToNode(from_index) in self.origins else 1

        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,
            self.capacities,
            True,
            'Capacity'
        )

        distance_dimension = routing.GetDimensionOrDie('Distance')
        distance_dimension.SetGlobalSpanCostCoefficient(10000)

        search_parameter = pywrapcp.DefaultRoutingSearchParameters()
        search_parameter.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        assignment = routing.SolveWithParameters(search_parameter)

        if assignment:
            return print_solution(manager, routing, assignment)
