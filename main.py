import json

from shapely import Point

from Model.range import Range
from Utils.draw import DrawTool
from Logic.engine_eskimo import EngineEskimo
from Configuration.configuration_handler import Configurations


FILE_PATH = r"Configuration/configuration.json"

config = Configurations(FILE_PATH)

# TODO: delete this

engine = EngineEskimo(start_position = config.get_start_position(),
                      end_position = config.get_end_position(),
                      number_of_polygons_range = Range(**config.get_number_of_polygons_range()),
                      num_of_points_in_polygon_range = Range(**config.get_number_of_points_in_polygon_range()),
                      polygon_radius_range = Range(**config.get_polygon_radius_range()),
                      surface_size = config.get_surface_size())

drawTool = DrawTool(config.get_surface_size())

# draw polygons TODO: create first by engine the polygons, and receive the list of them
for i in range(engine.get_number_of_polygons()):
    points, convex_hull = engine.create_valid_polygon()
    drawTool.draw_convex_hulls(points, convex_hull,"Iceberg " + str(i + 1))

# add start_end_points
drawTool.draw_point(config.get_start_position(),"start",'green')
drawTool.draw_point(config.get_end_position(),"end",'red')

drawTool.show()

#  data to write to the JSON file
data = engine.get_metadata()

# file path where the JSON data will be written
file_path = 'Data/data.json'

# write data to JSON file
with open(file_path, 'w') as file:
    json.dump(data, file, indent=4)  # `indent=4` formats the JSON data for readability

print(f"Data successfully written to {file_path}")





