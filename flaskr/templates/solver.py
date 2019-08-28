from abc import ABC, abstractmethod
import numpy as np
import math
from typing import List


class BaseSolver(ABC):
    """Base class for creating new solver for CVRP

    Attributes:
        num_locations: An integer count of locations
        distance_matrix: A 2D matrix, m, where m[i][j] is the distance between location i and j
        capacities: A list, l, of integer where l[i] is the capacity of vehicle i
        origins: A list, l, of integer where l[i] is the index of starting location for vehicle i
        destination: A integer representing the index of the destination location
    """
    def __init__(self,
                 locations: List[List[float]],
                 capacities: List[int],
                 origins: List[int],
                 destination: int = 0
                 ) -> None:
        """Convert input format to initialize the class

        Args:
            locations: A 2D array, a, where a[0][i] and a[1][i] represents the coordinate of location i.
            capacities: A list, l, of integer where l[i] is the capacity of vehicle i
            origins: A list, l, of integer where l[i] is the index of starting location for vehicle i
            destination: A integer representing the index of the destination location
        """
        # self.num_locations = len(locations[0])
        # self.distance_matrix = np.zeros((self.num_locations, self.num_locations))
        self.num_locations = len(locations[0])
        # print(self.num_locations)
        self.distance_matrix = locations
        self.capacities = capacities
        self.origins = origins
        self.destination = destination

        # for i in range(self.num_locations):
        #     for j in range(i):
        #         self.distance_matrix[i][j] = \
        #             math.sqrt((locations[0][i] - locations[0][j]) ** 2 + (locations[1][i] - locations[1][j]) ** 2)
        #         self.distance_matrix[j][i] = self.distance_matrix[i][j]

    @abstractmethod
    def solve(self) -> List[List[int]]:
        return NotImplemented
