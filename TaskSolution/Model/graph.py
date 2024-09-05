from pydantic import BaseModel
from shapely import Point
from TaskSolution.Model.edge import Edge


class Graph(BaseModel):
    points: list[Point] = []
    edges: list[Edge] = []
    points_neighbours : dict[Point, set[Point]]

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def complete_graph_from_points(cls, points: list[Point]):
        pass
        # edges = []
        #
        # # create edges between all the points ( undirected graph - each edge represented once regardless direction )
        # for point in points:
        #     for another_point in points:
        #         if point == another_point:
        #             continue
        #
        #
        # return cls(points=points, edges=[])

    def add_point(self,point : Point):
        if not isinstance(point, Point):
            raise ValueError('Point must be of type Point')
        self.points.append(point)

    def add_edge(self, point1: Point, point2: Point):
        if point1 not in self.points or point2 not in self.points:
            raise ValueError("Both points must be in the graph.")
        self.edges.append(Edge(point1=point1, point2=point2))

    def get_edges(self) -> list[Edge]:
        return self.edges

    def get_points(self) -> list[Point]:
        return self.points