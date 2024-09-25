import random

import numpy as np
from pydantic import BaseModel
from scipy.constants import point
from scipy.spatial import KDTree
from shapely import Point, Polygon
from shapely.lib import distance

from Statistics.statistics_singleton import StatisticsSingleton
from TaskSolution.Model.graph import Graph
from TaskSolution.Model.undirected_edge import UndirectedEdge


class RrtNode:
    def __init__(self, point: Point,parent = None ):
        self.point = point
        self.parent = parent
        self.cost = float('inf')  # Cost from start to this node

class GraphBuilder(BaseModel):
    """
    this class responsible to construct a Graph object.

    parameters
    start_point:Point
    end_point:Point
    polygons : list[Polygon]
    """
    polygons : list[Polygon]
    start_point : Point
    end_point : Point


    class Config:
        arbitrary_types_allowed = True

    def _unpack_points_from_polygons(self) -> list[Point]:
        points = []
        for polygon in self.polygons:
            for point in polygon.exterior.coords:
                points.append(Point(point))
        return points

    def prm(self,num_samples,connect_radius,surface_size) -> Graph:
        """ the number of """
        # add statistics
        statistic = StatisticsSingleton()
        statistic.prm_num_of_samples = num_samples
        statistic.prm_radius = connect_radius
        points:list[Point] = [self.start_point, self.end_point]

        # Randomly sample points
        for _ in range(num_samples - 2):
            x = random.randint(0,surface_size - 1)
            y = random.randint(0,surface_size - 1)
            is_point_in_polygon = False
            for polygon in self.polygons:
                if polygon.contains(Point(x, y)):
                    is_point_in_polygon = True
            if not is_point_in_polygon:
                points.append(Point(x, y))

        # Convert the list of Point objects to a list of tuples
        point_tuples = [(point.x, point.y) for point in points]

        # Build the graph
        kdtree = KDTree(point_tuples)

        edges = []

        for point_tuple in point_tuples:
            idxs = kdtree.query_ball_point(point_tuple, connect_radius) # get all the indexes of points in radius
            for neighbor in [points[i] for i in idxs if points[i] != point_tuple]: # for every neighbor point
                new_edge = UndirectedEdge(point1 = Point(point_tuple), point2 = Point(neighbor))
                if not new_edge.is_in_polygons(self.polygons):
                    edges.append(new_edge)

        return Graph(points = points, edges = edges)

    def _randomly_sample_valid_point(self,surface_size):
        is_point_in_polygon = True
        x = 0
        y = 0
        while is_point_in_polygon or not(0 <= x <= surface_size and 0 <= y <= surface_size):
            x = random.randint(0, surface_size - 1)
            y = random.randint(0, surface_size - 1)
            is_point_in_polygon = False
            for polygon in self.polygons:
                if polygon.contains(Point(x, y)):
                    is_point_in_polygon = True
        return Point(x, y)

    def _randomly_sample_valid_point_in_radius(self,center:Point, radius:float,surface_size) -> Point:
        is_valid_point = False
        x = 0
        y = 0
        while not is_valid_point or not(0 <= x <= surface_size and 0 <= y <= surface_size):
            # generate a random angle between 0 and 2*pi
            angle = np.random.uniform(0, 2 * np.pi)

            # generate a random radius between 0 and max_radius, ensuring uniform distribution
            random_radius = np.sqrt(np.random.uniform(0, radius ** 2))

            # convert polar coordinates (radius, angle) to cartesian coordinates (x, y)
            x = center.x + random_radius * np.cos(angle)
            y = center.y + random_radius * np.sin(angle)

            is_valid_point = True # first assume the point is ok
            if x < 0 or y < 0 or x >= surface_size or y >= surface_size:
                is_valid_point = False
                continue

            edge = UndirectedEdge(point1=Point(x,y), point2=center)
            if edge.is_in_polygons(self.polygons):
                is_valid_point = False
                continue

            for polygon in self.polygons:
                if polygon.contains(Point(x, y)):
                    is_valid_point = False


        return Point(x, y)

    # def _steer(self,from_point, to_point,step_size) -> Point:
    #     direction = to_point - from_point
    #     distance_to_target = distance(from_point, to_point)
    #     if distance_to_target < step_size:
    #         return from_point
    #     else:
    #         direction = direction / distance_to_target # normalize

    def rewire(self,tree,new_node,radius):
        neighboors = []
        for node in tree:
            if distance(new_node.point, node.point) < radius:
                neighboors.append(node)

        for neighbor in neighboors:
            potential_cost = (new_node.cost + distance(new_node.point, neighbor.point))
            if potential_cost < neighbor.cost:
                # check if we will rewire, if edge will not cross polygon
                edge = UndirectedEdge(point1=neighbor.point, point2=new_node.point)
                if not edge.is_in_polygons(self.polygons):
                    # rewire
                    neighbor.parent = new_node
                    neighbor.cost = potential_cost

    @staticmethod
    def _build_graph_from_tree(tree) -> Graph:
        points = []
        edges = []

        for node in tree:
            points.append(node.point)
            if node.parent is not None:
                new_edge = UndirectedEdge(point1 = node.point, point2 = node.parent.point)
                edges.append(new_edge)
        return Graph(points = points,edges = edges)

    def rrt_star(self,surface_size) -> Graph:
        # initialization
        start_node = RrtNode(self.start_point)
        start_node.cost = 0
        tree = [start_node]
        step_size = 20
        neighborhood_radius = 50
        max_iterations = 2000
        for _ in range(max_iterations):
            # generate random sample
            random_point = self._randomly_sample_valid_point(surface_size)
            # find nearest node
            nearst_node = min(tree, key=lambda node: distance(node.point, random_point))
            # generate a point that close to the nearset point
            new_point = self._randomly_sample_valid_point_in_radius(nearst_node.point, step_size,surface_size)
            new_node = RrtNode(new_point,nearst_node)
            # add node to the tree
            new_node.cost = nearst_node.cost + distance(nearst_node.point, new_point)
            tree.append(new_node)
            # check goal condition
            edge = UndirectedEdge(point1=new_point, point2=self.end_point)
            if distance(new_point,self.end_point) < step_size and not edge.is_in_polygons(self.polygons):
                # add the end node, and return the graph
                end_node = RrtNode(self.end_point,new_node)
                tree.append(end_node)
                graph = self._build_graph_from_tree(tree)
                return graph
            # rewire the tree
            self.rewire(tree,new_node,neighborhood_radius)
        return self._build_graph_from_tree(tree)


    def build(self,surface_size,build_with_prm = False) -> Graph:
        # if build_with_prm:
        #     num_samples = int(surface_size / 1.5)
        #     connect_radius = int(surface_size / 10)
        #     return self.prm(num_samples,connect_radius,surface_size)
        if build_with_prm:
            num_samples = int(surface_size / 1.5)
            connect_radius = int(surface_size / 10)
            return self.rrt_star(surface_size)

        points = self._unpack_points_from_polygons()
        points.append(self.start_point)
        points.append(self.end_point)
        edges = []

        for point in points:
            for another_point in points:
                if point == another_point:
                    continue

                new_edge = UndirectedEdge(point1 = point, point2 = another_point)

                # check if the edge overlapping the polygons
                edge_in_polygon = False
                for polygon in self.polygons:
                    if new_edge.is_in_polygon(polygon):
                        edge_in_polygon = True

                if not edge_in_polygon and new_edge not in edges:
                    edges.append(new_edge)



        return Graph(points = points, edges = edges)


