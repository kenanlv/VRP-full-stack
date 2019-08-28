from .solver import BaseSolver
from typing import List


class Vehicle:
    # vehId
    # Route
    # capacity
    # load
    # curLoc
    # CLosed
    # route = []
    # load = 0

    def __init__(self, id, capacity, cur_location):
        self.id = id
        self.capacity = capacity
        self.load = 0
        self.cur_location = cur_location
        self.closed = False
        self.route = []

    def add_node(self, cus_node):
        self.route.append(cus_node)
        self.cur_location = cus_node.id
        self.load += cus_node.demand
        # print("when add node, load: ", self.load, "goto location: ", self.cur_location)
        # add self and destination makes load goes to 5

    def check_fit(self, demand) -> bool:
        # print("in check_fit, compare load, capacity, and result:  ",self.load, self.capacity, self.load <=
        # self.capacity)
        return self.load + demand <= self.capacity


class Node:
    # id = 0
    # x_pos = 0
    # y_pos = 0
    # isDriver = False
    # isDepot = True
    # isRouted = False
    def __init__(self, id, is_driver, is_routed, is_depot=False, demand=1):
        self.id = id
        self.is_routed = is_routed
        self.is_depot = is_depot
        self.is_driver = is_driver
        self.demand = demand


def not_finished(point) -> bool:
    for i in range(1, len(point)):
        # if not point[i].is_driver and not point[i].is_routed:
        if not point[i].is_routed:
            return True
    return False


"""
Base class for creating new solver for CVRP
Attributes:
    num_locations: An integer count of locations
    distance_matrix: A 2D matrix, m, where m[i][j] is the distance between location i and j
    capacities: A list, l, of integer where l[i] is the capacity of vehicle i
    origins: A list, l, of integer where l[i] is the index of starting location for vehicle i
    destination: A integer representing the index of the destination location
"""


class SolverNotGoogle(BaseSolver):
    cost = 0
    vehi = None
    # point = None

    def solve(self) -> List[List[int]]:  # every path in list: from -> to
        num_locations = self.num_locations
        # print(num_locations)
        distance_mx = self.distance_matrix
        capacities = self.capacities
        origins = self.origins
        depot = Node(self.destination, False, False, True, 0)
        self.point = [None] * num_locations
        # print(num_locations)
        # print(len(self.point))
        # print("destiniation: ", self.destination)
        self.point[0] = depot
        # for i in origins:
        #     print(i)
        # Construct all nodes with Driver and Customer
        for i in range(1, len(self.point)):
            if i in origins:
                self.point[i] = Node(i, True, False, False, 0)
                # print("is dirver ", i)
                # origins.remove(i)
            else:
                self.point[i] = Node(i, False, False)
                # print("is customer ", i)
        # Construct Vehicles
        self.vehi = [None] * len(self.origins)
        for i in range(len(self.vehi)):
            cur_loc = self.origins[i]
            self.vehi[i] = Vehicle(cur_loc, capacities[i], cur_loc)
            # print("init vehi[] cur_loc, capacities, curloc", cur_loc,capacities[i],cur_loc)
        # print("len of vehi[] ", len(self.vehi))
        self.greedy_solution(distance_mx)
        self.inter_route_location_search()
        self.intra_route_local_search()
        ret = []
        vehi_idx = 1
        for i in self.vehi:
            temp = []
            print("Route for vehicle ", vehi_idx, ": ")

            for j in i.route:
                print(j.id, " -> ", end=" ")
                temp.append(j.id)
            ret.append(temp)
            print(temp)
            print(" ")
            vehi_idx += 1
        # print(ret)
        print("Total solution cost: ", self.cost)
        return ret

    def greedy_solution(self, distance_mx):
        candi_cost = 0.0
        end_cost = 0.0
        vehi_idx = 0

        while not_finished(self.point):

            cust_idx = 0
            min_cost = float("inf")
            candidate = None
            # print("num of car: ", len(self.origins))
            if not self.vehi[vehi_idx].route:
                self.vehi[vehi_idx].add_node(self.point[self.vehi[vehi_idx].cur_location])
                # print("should add idx one: ", vehi_idx)
            for i in range(1, self.num_locations):
                if not self.point[i].is_driver and not self.point[i].is_routed:
                    if self.vehi[vehi_idx].check_fit(self.point[i].demand):
                        candi_cost = distance_mx[self.vehi[vehi_idx].cur_location][i]
                        if min_cost > candi_cost:
                            min_cost = candi_cost
                            cust_idx = i
                            candidate = self.point[i]
                            # print("in arrange: ", candidate.id)
            if not candidate:
                if vehi_idx + 1 < len(self.vehi):
                    if self.vehi[vehi_idx].cur_location != 0:
                        end_cost = distance_mx[self.vehi[vehi_idx].cur_location][0]
                        self.vehi[vehi_idx].add_node(self.point[0])
                        self.cost += end_cost
                    vehi_idx += 1
                else:
                    print("unable to process, in greedySolution after candidate been none")
                    break
            else:
                self.vehi[vehi_idx].add_node(candidate)
                self.point[cust_idx].is_routed = True
                self.cost += min_cost
        end_cost = distance_mx[self.vehi[vehi_idx].cur_location][0]
        self.vehi[vehi_idx].add_node(self.point[0])
        self.cost += end_cost

    def inter_route_location_search(self):
        route_from = []
        route_to = []
        moving_demand = 0

        vehi_idx_from = None
        vehi_idx_to = None
        best_n_cost = None
        neibor_cost = None

        swap_idx_a = -1
        swap_idx_b = -1
        swap_route_from = -1
        swap_route_to = -1

        max_ite = 100000
        ite_num = 0
        termination = False
        while not termination:
            ite_num += 1
            best_n_cost = float("inf")
            for vehi_idx_from in range(len(self.vehi)):
                route_from = self.vehi[vehi_idx_from].route
                route_from_len = len(route_from)
                for i in range(1, route_from_len - 1):
                    for vehi_idx_to in range(len(self.vehi)):
                        route_to = self.vehi[vehi_idx_to].route
                        route_to_len = len(route_to)
                        for j in range(route_to_len - 1):
                            moving_demand = route_from[i].demand
                            if vehi_idx_from == vehi_idx_to or self.vehi[vehi_idx_to].check_fit(moving_demand):
                                if vehi_idx_from == vehi_idx_to and not (j == i or j == i - 1):
                                    minus_cost1 = self.distance_matrix[route_from[i - 1].id][route_from[i].id]
                                    minus_cost2 = self.distance_matrix[route_from[i].id][route_from[i + 1].id]
                                    minus_cost3 = self.distance_matrix[route_to[j].id][route_to[j + 1].id]

                                    add_cost1 = self.distance_matrix[route_from[i - 1].id][route_from[i + 1].id]
                                    add_cost2 = self.distance_matrix[route_to[j].id][route_from[i].id]
                                    add_cost3 = self.distance_matrix[route_from[i].id][route_to[j + 1].id]

                                    neibor_cost = add_cost1 + add_cost2 + add_cost3 \
                                                  - minus_cost1 - minus_cost2 - minus_cost3
                                    if neibor_cost < best_n_cost:
                                        best_n_cost = neibor_cost
                                        swap_idx_a = i
                                        swap_idx_b = j
                                        swap_route_from = vehi_idx_from
                                        swap_route_to = vehi_idx_to
            if best_n_cost < 0:
                route_from = self.vehi[swap_route_from].route
                route_to = self.vehi[swap_route_to].route

                # self.vehi[swap_route_from].route.clear() #Not sure what to do here
                # self.vehi[swap_route_to].route.clear()
                # del self.vehi[swap_route_from].route[:]
                # del self.vehi[swap_route_to].route[:]

                self.vehi[swap_route_from].route = None
                self.vehi[swap_route_to].route = None

                swap_node = route_from[swap_idx_a]
                route_from.pop(swap_idx_a)

                if swap_route_from == swap_route_to:
                    if swap_idx_a < swap_idx_b:
                        route_to.insert(swap_idx_b, swap_node)
                    else:
                        route_to.insert(swap_idx_b + 1, swap_node)
                else:
                    route_to.insert(swap_idx_b + 1, swap_node)

                self.vehi[swap_route_from].route = route_from
                # self.vehi[swap_route_from].load -= MoveingDemand for custom demand
                self.vehi[swap_route_from].load -= moving_demand

                self.vehi[swap_route_to].route = route_to
                self.vehi[swap_route_to].load += moving_demand

                self.cost += best_n_cost
            else:
                termination = True
            if ite_num == max_ite:
                termination = True

    def intra_route_local_search(self):
        rt = []
        best_n_cost = None
        neighbor_cost = None

        swap_idx_a = -1
        swap_idx_b = -1
        swap_route = -1

        max_ite = 100000
        ite_num = 0
        termination = False
        while not termination:
            ite_num += 1
            best_n_cost = float("inf")
            for vehi_idx in range(len(self.vehi)):
                rt = self.vehi[vehi_idx].route
                route_len = len(rt)
                for i in range(1, route_len - 1):
                    for j in range(route_len - 1):
                        if j != i and j != i - 1:
                            minus_cost1 = self.distance_matrix[rt[i - 1].id][rt[i].id]
                            minus_cost2 = self.distance_matrix[rt[i].id][rt[i + 1].id]
                            minus_cost3 = self.distance_matrix[rt[j].id][rt[j + 1].id]

                            add_cost1 = self.distance_matrix[rt[i - 1].id][rt[i + 1].id]
                            add_cost2 = self.distance_matrix[rt[j].id][rt[i].id]
                            add_cost3 = self.distance_matrix[rt[i].id][rt[j + 1].id]

                            neighbor_cost = add_cost1 + add_cost2 + add_cost3 \
                                          - minus_cost1 - minus_cost2 - minus_cost3
                            if neighbor_cost < best_n_cost:
                                best_n_cost = neighbor_cost
                                swap_idx_a = i
                                swap_idx_b = j
                                swap_route = vehi_idx
            if best_n_cost < 0:
                rt = self.vehi[swap_route].route
                swap_node = rt[swap_idx_a]

                rt.pop(swap_idx_a)

                if swap_idx_a < swap_idx_b:
                    rt.insert(swap_idx_b, swap_node)
                else:
                    rt.insert(swap_idx_b + 1, swap_node)
            else:
                termination = True
            if ite_num == max_ite:
                termination = True