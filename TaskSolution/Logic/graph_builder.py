from collections import defaultdict

from pydantic import BaseModel, Field
from shapely import Point, Polygon
from TaskSolution.Model.edge import Edge
from TaskSolution.Model.graph import Graph


class GraphBuilder(BaseModel):
    """
    this class responsible to construct a Graph object.

    parameters
    start_point:Point
    end_point:Point
    polygons : list[Polygon]
    """
    _points : list[Point] = []
    polygons : list[Polygon]
    _points_neighbours : dict[Point, set[Point]] = {}
    _edges : list[Edge] = []
    start_point : Point
    end_point : Point

    def __init__(self, **data):
        super().__init__(**data)
        self._unpack_points_from_polygons()
        self._points.append(self.start_point)
        self._points.append(self.start_point)

    class Config:
        arbitrary_types_allowed = True

    def _unpack_points_from_polygons(self):
        for polygon in self.polygons:
            for point in polygon.exterior.coords:
                self._points.append(Point(point))


    def build(self) -> Graph:
        for point in self._points:
            for another_point in self._points:
                if point == another_point:
                    continue

                new_edge = Edge(point1 = point,point2 = another_point)
                self._edges.append(new_edge)
                if point in self._points_neighbours:
                    self._points_neighbours[point].add(another_point)
                else:
                    self._points_neighbours[point] = {another_point, }

        # delete the edges if they inside the polygon, and update the points neighbours
        for edge in self._edges:
            for polygon in self.polygons:
                if edge.is_in_polygon(polygon):
                    try:
                        self._points_neighbours[edge.point1].remove(edge.point2)
                        self._points_neighbours[edge.point2].remove(edge.point1)
                    except KeyError: pass

        # TODO: pass a copy and not the reference
        return Graph(points = self._points, edges = self._edges, points_neighbours = self._points_neighbours)


