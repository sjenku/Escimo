from xmlrpc.client import DateTime
import csv
import os

class Statistics:
    """ singleton class, responsible to add the data """

    build_graph_algo:str
    build_graph_time:DateTime
    find_path_time:DateTime
    number_of_nodes:int
    number_of_edges:int
    number_of_polygons:int


    def write(self):

        filename = 'statistics.csv'

        # Check if the file exists
        file_exists = os.path.isfile(filename)

        # Open the file in append mode if it exists, otherwise create a new file
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Write the header row if the file is new
            if not file_exists:
                writer.writerow(['build graph algo','build graph time', 'find path time', 'number of nodes', 'number of edges', 'number of polygons'])

            # Define the new data to be added
            new_data = [self.build_graph_algo,
                        self.build_graph_time,
                        self.find_path_time,
                        self.number_of_nodes,
                        self.number_of_edges,
                        self.number_of_polygons]

            # Write the new data row
            writer.writerow(new_data)

        print(f"Data has been added to {filename}")

