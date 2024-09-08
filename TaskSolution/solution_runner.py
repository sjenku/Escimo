import json

from shapely import Point
from shapely.lib import polygons

from Module.engine_data import EngineData
from TaskSolution.Logic.graph_builder import GraphBuilder
from Utils.converter import Converter


class SolutionRunner:
    @staticmethod
    def run():
        print("Solution Runner run ")
        file_path = r"TaskCreator/Data/data.json"

        with open(file_path, 'r') as file:
            # load the JSON and parse this json
            data = json.load(file)
            engine_data = EngineData(**data)
            print(engine_data)

        # create a list of polygons from the data
        polygons_list = []
        for iceberg in engine_data.icebergs:
            polygon = Converter.to_polygon(iceberg)
            polygons_list.append(polygon)

        # get the start and end points
        start_point = Point(engine_data.start_x, engine_data.start_y)
        end_point = Point(engine_data.target_x, engine_data.target_y)

        # build the graph
        graph_builder = GraphBuilder(start_point=start_point, end_point=end_point, polygons=polygons_list)
        graph = graph_builder.build()

        graph.print()
