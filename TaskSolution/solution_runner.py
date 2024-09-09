import json
from datetime import datetime

from shapely import Point
from Module.engine_data import EngineData
from TaskSolution.Logic.graph_builder import GraphBuilder
from TaskSolution.Logic.solution_handler import SolutionHandler
from Utils.converter import Converter
from Utils.draw import DrawTool


class SolutionRunner:
    @staticmethod
    def run(draw_tool:DrawTool):
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
        start_time = datetime.now()  # record the start time
        graph = graph_builder.prm(engine_data.icebergs_count * 50,50) #TODO: handle magic numbers
        end_time = datetime.now() # record the end time
        print("Graph Time Build => ", end_time - start_time)

        # graph.print()

        # draw to the screen the graph
        for edge in graph.edges:
            draw_tool.draw_line_between_points(edge.point1, edge.point2)

        # run the solution:
        solution_handler = SolutionHandler()
        start_time = datetime.now()  # record the start time
        solution = solution_handler.a_star(graph,start_point,end_point)
        end_time = datetime.now() # record the end time
        print("Find The Path => ", end_time - start_time)

        # draw the path
        solution_edges = solution_handler.point_path_to_edges(solution)
        for i,edge in enumerate(solution_edges):
            draw_tool.draw_line_between_points(edge.point1, edge.point2,"green",f"Edge{i+1}",True)


