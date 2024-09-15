import json
from datetime import datetime

from Statistics.statistics_singleton import StatisticsSingleton
from TaskCreator.Logic.engine_eskimo import EngineEskimo
from Utils.draw import DrawTool
from Configuration.configuration import Configurations


class TaskRunner:

    @staticmethod
    def run(draw_tool: DrawTool,config: Configurations):

        # handle statistics
        statistics = StatisticsSingleton()

        engine = EngineEskimo(start_pos=config.start_position.point(),
                              end_pos=config.end_position.point(),
                              number_of_polygons_range=config.number_of_polygons_range,
                              num_of_points_in_polygon_range=config.number_of_points_in_polygon_range,
                              polygon_radius_range=config.polygon_radius_range,
                              surface_size=config.surface_size)


        print("number of polygons: ", engine.get_number_of_polygons())
        statistics.number_of_polygons = engine.get_number_of_polygons()
        statistics.polygons_radius_from = config.polygon_radius_range.from_
        statistics.polygons_radius_to = config.polygon_radius_range.to
        statistics.distance_start_to_end_point = config.start_position.point().distance(config.end_position.point())

        # create polygons
        cunvex_hulls = []
        points = []
        start_time = datetime.now()
        for i in range(engine.get_number_of_polygons()):
            point, convex = engine.create_valid_polygon()
            cunvex_hulls.append(convex)
            points.append(point)
        end_time = datetime.now()
        print("Build polygons => ",end_time - start_time)

        # draw polygons TODO: create first by engine the polygons, and receive the list of them
        for i in range(engine.get_number_of_polygons()):
            draw_tool.draw_convex_hulls(points[i], cunvex_hulls[i], "Iceberg " + str(i + 1))

        # add start_end_points
        draw_tool.draw_point(config.start_position.point(), "start", 'green')
        draw_tool.draw_point(config.end_position.point(), "end", 'red')


        #  data to write to the JSON file
        data = engine.get_data()

        # file path where the JSON data will be written
        file_path = 'TaskCreator/Data/data.json'

        # write data to JSON file
        with open(file_path, 'w') as file:
            json.dump(data.model_dump(), file, indent=4)  # `indent=4` formats the JSON data for readability

        print(f"Data successfully written to {file_path}")
