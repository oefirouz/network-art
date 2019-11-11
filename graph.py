#graph class has a dict of vertex objects, which contain (x,y) and name of vertex
#coordinates are center of circle

class Vertex:
    def __init__(self, vtx_num, x, y):
        self.vtx_num = vtx_num
        self.x_coord = x
        self.y_coord = y

class Graph:
    def __init__(self, numvertex):
        self.adjMatrix = [[-1] * numvertex for x in range(numvertex)]
        self.numvertex = numvertex
        self.vertices = {}
        self.verticeslist = [0] * numvertex

    def set_vertex(self, vtx, id, x, y):
        if 0 <= vtx <= self.numvertex:
            self.vertices[id] = Vertex(vtx, x, y)
            self.verticeslist[vtx] = id

    def set_edge(self, frm, to, cost=0):
        frm = self.vertices[frm].vtx_num
        to = self.vertices[to].vtx_num
        self.adjMatrix[frm][to] = cost
        self.adjMatrix[to][frm] = cost

    def get_vertex(self):
        return self.verticeslist

    def get_coordinates(self, id):
        x_y = (self.vertices[id].x_coord, self.vertices[id].y_coord)
        return x_y

    def get_edges(self):
        edges = []
        for i in range(self.numvertex):
            for j in range(self.numvertex):
                if (self.adjMatrix[i][j] != -1):
                    edges.append([self.verticeslist[i], self.verticeslist[j], self.adjMatrix[i][j]])
        return edges

    def get_matrix(self):
        return self.adjMatrix

