import json

from Configuration.configuration import Configurations
from Statistics.statistics_singleton import StatisticsSingleton
from TaskCreator.task_runner import TaskRunner
from TaskSolution.solution_runner import SolutionRunner
from Utils.draw import DrawTool

file_path = r"Configuration/configuration.json"

with open(file_path, 'r') as file:
    # load the JSON data into a Configurations object
    data = json.load(file)
    config = Configurations(**data)

# create the draw tool to draw the outputs
draw_tool = DrawTool(surface_size= config.surface_size)

taskRunner = TaskRunner()
taskRunner.run(draw_tool= draw_tool,config= config)

solutionRunner = SolutionRunner()
solutionRunner.run(draw_tool= draw_tool,config= config)

draw_tool.show()

statistics = StatisticsSingleton()
statistics.write()


