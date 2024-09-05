from collections import defaultdict

from pydantic import BaseModel, Field
from shapely import Point, Polygon
from TaskSolution.Model.edge import Edge
from TaskSolution.Model.graph import Graph


class GraphBuilder(BaseModel):
    points : list[Point] = []
    polygons : list[Polygon]
    points_neighbours : dict[Point, set[Point]] = {}
    edges : list[Edge] = []
    start_point : Point
    end_point : Point

    def __init__(self, **data):
        super().__init__(**data)
        self._unpack_points_from_polygons()
        self.points.append(self.start_point)
        self.points.append(self.start_point)


    def _unpack_points_from_polygons(self):
        for polygon in self.polygons:
            for point in polygon.coords:
                self.points.append(point)


    def build(self) -> Graph:
        graph = Graph()
        for point in self.points:
            for another_point in self.points:
                if point.equals(another_point):
                    continue

                new_edge = Edge(point1 = point,point2 = another_point)
                self.edges.append(new_edge)
                if point in self.points_neighbours:
                    self.points_neighbours[point].add(another_point)
                else:
                    self.points_neighbours[point] = {another_point,}

        # delete the edges if they inside the polygon, and update the points neighbours
        for edge in self.edges:
            for polygon in self.polygons:
                if edge.is_in_polygon(polygon):
                    try:
                        self.points_neighbours[edge.point1].remove(edge.point2)
                        self.points_neighbours[edge.point2].remove(edge.point1)
                    except KeyError: pass

        return Graph()


