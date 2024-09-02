import json

from Data.engine_data import EngineData
from Model.iceberg import Iceberg
from Utils.draw import DrawTool
from Logic.engine_eskimo import EngineEskimo
from Configuration.configuration import Configurations


FILE_PATH = r"Configuration/configuration.json"

with open(FILE_PATH, 'r') as file:
    # load the JSON data into a Configurations object
    data = json.load(file)
    config = Configurations(**data)


engine = EngineEskimo(start_pos = config.start_position.point(),
                      end_pos = config.end_position.point(),
                      number_of_polygons_range = config.number_of_polygons_range,
                      num_of_points_in_polygon_range = config.number_of_points_in_polygon_range,
                      polygon_radius_range = config.polygon_radius_range,
                      surface_size = config.surface_size)

drawTool = DrawTool(config.surface_size)

print("number of polygons: ",engine.get_number_of_polygons())
# draw polygons TODO: create first by engine the polygons, and receive the list of them
for i in range(engine.get_number_of_polygons()):
    points, convex_hull = engine.create_valid_polygon()
    drawTool.draw_convex_hulls(points, convex_hull,"Iceberg " + str(i + 1))

# add start_end_points
drawTool.draw_point(config.start_position.point(),"start",'green')
drawTool.draw_point(config.end_position.point(),"end",'red')

drawTool.show()

#  data to write to the JSON file
#data = engine.get_metadata()
data = engine.get_data()

# file path where the JSON data will be written
file_path = 'Data/data.json'

# write data to JSON file
with open(file_path, 'w') as file:
    json.dump(data.model_dump(), file, indent=4)  # `indent=4` formats the JSON data for readability

print(f"Data successfully written to {file_path}")





