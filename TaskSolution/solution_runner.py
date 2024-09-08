import json
from TaskSolution.Model.input_data import InputData


class SolutionRunner:
    @staticmethod
    def run():
        print("Solution Runner run ")
        file_path = r"TaskCreator/Data/data.json"

        with open(file_path, 'r') as file:
            # load the JSON data into a Configurations object
            data = json.load(file)
            input_data = InputData(**data)
            print(input_data)

