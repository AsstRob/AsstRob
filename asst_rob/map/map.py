from asst_rob.core.directions import Directions
left = 0
front = 1
right = 2
back = 3
vertices = {}
prv_vertex = "initial"
path_stack = []
location = 0


class Vertex:
    def __init__(self, name, distance):
        self.name = name
        self.distance = distance

    def get_name(self):
        return self.name

    def get_distance(self):
        return self.distance


def add_vertex(name, prv, dep_direction, distance):
    if name not in vertices.keys():
        vertices[name] = [Vertex]*4
        vertices[name][back] = Vertex(prv, distance)

        if prv != "Non":
            vertices[prv][dep_direction] = Vertex(name, distance)

        print("Vertex created : " + name)

        return True
    else:
        return False


def add_edge(u, v, dep_direction, arr_direction, distance):
    if u in vertices.keys() and v in vertices.keys():
        vertices[u][dep_direction] = Vertex(v, distance)
        vertices[v][arr_direction] = Vertex(u, distance)
        print("Edge added : " + u + " -> " + v)

        return True
    else:
        return False


def init_map():
    add_vertex("A", "Non", 0, 0)
    add_vertex("B", "A", front, 20)
    add_vertex("C", "B", front, 30)
    add_vertex("D", "C", front, 10)
    add_vertex("E", "C", left, 35)
    add_vertex("F", "E", right, 40)
    add_vertex("G", "E", front, 10)
    add_vertex("H", "E", left, 25)
    add_vertex("I", "H", right, 50)
    add_vertex("J", "C", right, 45)
    add_vertex("K", "J", right, 60)

    add_edge("B", "H", left, left, 60)

    return vertices
