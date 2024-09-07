from pydantic import BaseModel
from shapely import Point
from TaskSolution.Model.edge import Edge
import logging



class Graph(BaseModel):
    points: list[Point] = []
    edges: list[Edge] = []
    _points_neighbours : dict[Point, set[Point]] = {}# for every point, hold who is the neighbours of that point
    _logger : logging.Logger = logging.getLogger(__name__)

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        # Configure logging to show INFO level messages
        logging.basicConfig(level=logging.INFO,  # Ensure this is set to INFO or lower
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self._set_points_neighbours()

    def _set_points_neighbours(self):
        for edge in self.edges:
            point = edge.point1
            another_point = edge.point2
            if point in self._points_neighbours:
                self._points_neighbours[point].add(another_point)
            else:
                self._points_neighbours[point] = {another_point, }


    def print(self):
        self._logger.info(str(self))



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

    def __str__(self):
        st = "Graph : \n"
        st += "Points neighbours =================== : \n"
        for point in self._points_neighbours:
            st += f"{point}: {self._points_neighbours[point]}\n"
        st += "Edges =============================== : \n"
        for edge in self.edges:
            st += f"{edge}\n"
        return st

