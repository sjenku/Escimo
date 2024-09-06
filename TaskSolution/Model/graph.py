from pydantic import BaseModel
from shapely import Point
from TaskSolution.Model.edge import Edge
import logging



class Graph(BaseModel):
    points: list[Point] = []
    edges: list[Edge] = []
    points_neighbours : dict[Point, set[Point]]

    class Config:
        arbitrary_types_allowed = True



    def print(self):
        logger = logging.getLogger(__name__)
        # Configure logging to show INFO level messages
        logging.basicConfig(level=logging.INFO,  # Ensure this is set to INFO or lower
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger.info("Points Neighbours: ")
        logger.info(self.points_neighbours)



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