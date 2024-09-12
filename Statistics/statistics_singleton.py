from typing import Any
from xmlrpc.client import DateTime
import csv
import os

from pydantic import BaseModel


class StatisticsSingleton:
    """ singleton class, responsible to add the data """
    _instance = None

    build_graph_algo:str = ""
    build_graph_time:DateTime = None
    find_path_time:DateTime = None
    number_of_nodes:int = 0
    number_of_edges:int = 0
    number_of_polygons:int = 0
    prm_num_of_samples:int = 0
    prm_radius:float = 0.0

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        if not hasattr(self, 'initialized'):
            self.initialized = True

    def write(self):

        filename = 'statistics.csv'

        # Check if the file exists
        file_exists = os.path.isfile(filename)

        # Open the file in append mode if it exists, otherwise create a new file
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Write the header row if the file is new
            if not file_exists:
                writer.writerow(['build graph algo',
                                 'build graph time',
                                 'find path time',
                                 'number of nodes',
                                 'number of edges',
                                 'number of polygons',
                                 'prm_num_of_samples',
                                 'prm_radius'])

            # Define the new data to be added
            new_data = [self.build_graph_algo,
                        self.build_graph_time,
                        self.find_path_time,
                        self.number_of_nodes,
                        self.number_of_edges,
                        self.number_of_polygons,
                        self.prm_num_of_samples,
                        self.prm_radius]

            # Write the new data row
            writer.writerow(new_data)

        print(f"Data has been added to {filename}")

