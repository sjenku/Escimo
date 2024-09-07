from pydantic import BaseModel
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


