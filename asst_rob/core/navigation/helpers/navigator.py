from asst_rob.core.navigation.base_navigator import BaseNavigator
from asst_rob.map.map import *
from array import *


class Navigator(BaseNavigator):
    def __init__(self, start_vertex, end_vertex):
        super().__init__()
        self.map = init_map()

    @staticmethod
    def __get_location():
        location = input("Get location : ")
        return location

    def __get_path(self, start_vertex, end_vertex):
        diji = {}
        visited = {}

        for i in self.map.keys():
            if i == start_vertex:
                diji[i] = [0, ""]
            else:
                diji[i] = [float('inf'), ""]

            visited[i] = 0

        current_vertex = start_vertex

        while True:
            for i in self.map[current_vertex]:
                if isinstance(i, Vertex):
                    if diji[i.get_name()][0] > diji[current_vertex][0] + i.get_distance():
                        diji[i.get_name()][0] = diji[current_vertex][0] + i.get_distance()
                        diji[i.get_name()][1] = current_vertex

            visited[current_vertex] = 1
            min_vertex = ""
            min_val = float('inf')

            for i in self.map.keys():
                if min_val > self.map[i][0] and visited[i] == 0:
                    min_vertex = i
                    min_val = self.map[i][0]

            if min_vertex == "":
                """return path"""
            else:
                current_vertex = min_vertex
                visited[current_vertex] = 1

    def get_direction(self):
        return self.__direction