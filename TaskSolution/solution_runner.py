import json

from Module.engine_data import EngineData

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



        graph_builder = GraphBuilder(start_point=Point(1, 1), end_point=Point(5, 2), polygons=polygons)
