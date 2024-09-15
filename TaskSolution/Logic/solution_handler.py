import heapq
from itertools import combinations
from typing import Optional, List

from pydantic import BaseModel
from shapely import Point

from TaskSolution.Model.graph import Graph
from TaskSolution.Model.undirected_edge import UndirectedEdge


class SolutionHandler(BaseModel):

    # TODO: consider move the AStarItem to another file
    # class to handle the items inside the min-heap
    class AStarItem(BaseModel):
        priority:float # estimated cost to reach the goal
        g_score:float # cost to reach the item from the start item
        current_point:Point # this is the point of the current item
        path: list[Point] # the path to reach the current item

        class Config:
            arbitrary_types_allowed = True

        def __lt__(self, other):
            return self.priority < other.priority

        def __eq__(self, other):
            return self.priority == other.priority


    @staticmethod
    def _heuristic(point1: Point, point2: Point) -> float:
        """Compute the Euclidean distance between two points."""
        return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5


    def a_star(self,graph: Graph, start: Point, goal: Point) -> Optional[List[Point]]:
        """Perform A* algorithm to find the shortest path from start to goal in the graph."""
        open_set = []
        item = self.AStarItem(priority = (0 + self._heuristic(start,goal)), g_score = 0, current_point = start,path = [])
        heapq.heappush(open_set, item)
        came_from = {}
        g_score = {point: float('inf') for point in graph.points}
        g_score[start] = 0

        while open_set:
            item = heapq.heappop(open_set)

            if item.current_point == goal:
                return item.path + [item.current_point]

            for neighbor in graph.get_neighbours(item.current_point):
                tmp_g_score = item.g_score + self._heuristic(item.current_point, neighbor)
                if tmp_g_score < g_score[neighbor]:
                    came_from[neighbor] = item.current_point
                    g_score[neighbor] = tmp_g_score
                    f_score = tmp_g_score + self._heuristic(neighbor, goal)
                    new_item = self.AStarItem(priority = f_score, g_score = tmp_g_score, current_point = neighbor,path = item.path + [item.current_point])
                    heapq.heappush(open_set, new_item)

        return None

    @staticmethod
    def point_path_to_edges(points: List[Point]) -> List[UndirectedEdge]:
        """ convert path that represented as list of points, to a list of edges"""
        edges = []
        for i in range(len(points) - 1):
            point_from = points[i]
            point_to = points[i + 1]
            edges.append(UndirectedEdge(point1 = point_from, point2 = point_to))
        return edges

    @staticmethod
    def calculate_solution_distance(points: List[Point]) -> float:
        """ calculates the total distance of the path """
        path = SolutionHandler.point_path_to_edges(points)
        distance = 0.0
        for edge in path:
            distance += edge.length()
        return distance

