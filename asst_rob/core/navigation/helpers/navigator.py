from asst_rob.core.navigation.base_navigator import BaseNavigator
from asst_rob.map.map import *
path_stack = []
start = 0
prv_location = "Non"
Vertices = {}


class Navigator(BaseNavigator):
    def __init__(self, start_vertex, end_vertex):
        super().__init__()
        global Vertices
        Vertices = init_map()

        "Dijkstra algorithm"
        diji = {}
        visited = {}

        for i in self.Vertices.keys():
            if i == start_vertex:
                diji[i] = [0, ""]
            else:
                diji[i] = [float('inf'), ""]

            visited[i] = 0

        current_vertex = start_vertex

        while True:
            for i in self.Vertices[current_vertex]:
                if isinstance(i, Vertex) and i.get_name() != "Non":
                    if diji[i.get_name()][0] > diji[current_vertex][0] + i.get_distance():
                        diji[i.get_name()][0] = diji[current_vertex][0] + i.get_distance()
                        diji[i.get_name()][1] = current_vertex

            visited[current_vertex] = 1
            min_vertex = ""
            min_val = float('inf')

            for i in diji.keys():
                if min_val > diji[i][0] and visited[i] == 0:
                    min_vertex = i
                    min_val = diji[i][0]

            if min_vertex == "":
                while True:
                    path_stack.append(end_vertex)
                    if end_vertex == start_vertex:
                        break
                    else:
                        end_vertex = diji[end_vertex][1]
                break
            else:
                current_vertex = min_vertex
                visited[current_vertex] = 1

    def get_direction(self):
        crnt_location = path_stack.pop()
        global prv_location
        global start

        if len(path_stack) > 0:
            "Identify initial position"
            if start == 0:
                for i in range(4):
                    if not isinstance(vertices[crnt_location][i], Vertex):
                        continue

                    if Vertices[crnt_location][i] == path_stack.top():
                        prv_location = crnt_location
                        start = 1
                        if i == 0:
                            return Directions.LEFT
                        elif i == 1:
                            return Directions.FORWARD
                        elif i == 2:
                            return Directions.RIGHT
                        elif i == 3:
                            return Directions.REVERSE
            else:
                "Rotating and getting turn value"
                turn_val = 0
                for i in range(4):
                    if not isinstance(vertices[crnt_location][i], Vertex):
                        continue

                    if vertices[crnt_location][i].get_name() == prv_vertex:
                        turn_val = 3 - i
                        break

                for i in range(4):
                    if not isinstance(vertices[crnt_location][i], Vertex):
                        continue

                    if vertices[crnt_location][i].get_name() == path_stack[-1]:
                        new_i = (i + turn_val) % 4
                        if new_i == 0:
                            return Directions.LEFT
                        elif new_i == 1:
                            return Directions.FORWARD
                        elif new_i == 2:
                            return Directions.RIGHT
                        elif new_i == 3:
                            return Directions.REVERSE
        else:
            return 4
