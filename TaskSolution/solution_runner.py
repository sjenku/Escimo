import json
from datetime import datetime

from shapely import Point

from Configuration.configuration import Configurations
from Module.engine_data import EngineData
from Statistics.statistics_singleton import StatisticsSingleton
from TaskSolution.Logic.graph_builder import GraphBuilder
from TaskSolution.Logic.solution_handler import SolutionHandler
from Utils.draw import DrawTool


class SolutionRunner:
    @staticmethod
    def run(draw_tool:DrawTool,config:Configurations):

        # handle statistics
        statistic = StatisticsSingleton()

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
            polygon = iceberg.to_polygon()
            polygons_list.append(polygon)

        # get the start and end points
        start_point = Point(engine_data.start_x, engine_data.start_y)
        end_point = Point(engine_data.target_x, engine_data.target_y)

        # build the graph
        graph_builder = GraphBuilder(start_point=start_point, end_point=end_point, polygons=polygons_list)
        start_time = datetime.now()  # record the start time
        graph = graph_builder.build(build_with_prm=config.build_graph_with_prm,surface_size=config.surface_size)
        end_time = datetime.now()  # record the end time

        # add to statistics info
        statistic.build_graph_time = end_time - start_time
        statistic.number_of_nodes = len(graph.get_points())
        statistic.number_of_edges = len(graph.get_edges())
        if config.build_graph_with_prm:
            statistic.build_graph_algo = "prm"
        else:
            statistic.build_graph_algo = "node to node"

        print("Graph Time Build => ", statistic.build_graph_time)

        # draw to the screen the graph
        for edge in graph.edges:
            draw_tool.draw_line_between_points(edge.point1, edge.point2)

        # run the solution:
        solution_handler = SolutionHandler()
        start_time = datetime.now()  # record the start time
        solution = solution_handler.a_star(graph,start_point,end_point)
        end_time = datetime.now() # record the end time
        statistic.find_path_time = end_time - start_time
        print("Find The Path => ", statistic.find_path_time)

        # draw the path
        if solution is not None:
            statistic.found_path = True # update the statistics
            statistic.result_path_distance = solution_handler.calculate_solution_distance(solution)
            statistic.distance_diff = abs(statistic.distance_start_to_end_point - statistic.result_path_distance)
            solution_edges = solution_handler.point_path_to_edges(solution) # convert this list of points to edges
            for i,edge in enumerate(solution_edges):
                draw_tool.draw_line_between_points(edge.point1, edge.point2,"green",f"Edge{i+1}",True)
        else:
            statistic.found_path = False



