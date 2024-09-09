import random

from pydantic import BaseModel
from scipy.spatial import KDTree
from shapely import Point, Polygon
from TaskSolution.Model.graph import Graph
from TaskSolution.Model.undirected_edge import UndirectedEdge


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

    def prm(self,num_samples,connect_radius) -> Graph:
        """ the number of """
        points:list[Point] = [self.start_point, self.end_point]

        # Randomly sample points
        for _ in range(num_samples - 2):
            x = random.randint(0, 500 - 1)  #TODO: change to surface size
            y = random.randint(0, 500 - 1)
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


    def build(self) -> Graph:
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


