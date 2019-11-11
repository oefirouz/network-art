from PIL import Image, ImageDraw
import numpy as np
from graph import Graph
import collections

if __name__ == "__main__":
    w, h = 1024, 512
    data = np.zeros((h, w, 3), dtype=np.uint8)
    for i in range(50, 150):
        for j in range(50, 512):
            data[i, j] = [255,0,0]

    img = Image.fromarray(data, 'RGB')
    draw = ImageDraw.Draw(img)

    #this is basic graph
    G = Graph(3)
    G.set_vertex(0, 'a', 50, 50)
    G.set_vertex(1, 'b', 50, 150)
    G.set_vertex(2, 'c', 100, 100)
    G.set_edge('a', 'b', 10)
    G.set_edge('b', 'c', 20)
    G.set_edge('c', 'a', 30)

    print("Vertices of Graph")
    print(G.get_vertex())
    print("Edges of Graph")
    print(G.get_edges())
    print("Adjacency Matrix of Graph")
    print(G.get_matrix())
    print(G.get_coordinates("a"))

    #let's do a BFS!

    start = "a"
    end = "c"

    q = collections.deque()
    visited = set()
    q.append([start, start])
    res = [start]

    while q:
        n, path = q.popleft()
        visited.add(n)

        if n in G.get_vertex():
            for vertex in G.get_edges():
                start, end, cost = vertex
                if start == "a" and end not in visited:
                    visited.add(end)
                    q.append([end, path+end])
                    res.append(end)

    #draws circles: coordinates are center of circle
    for i in range(len(res)):
        x,y = G.get_coordinates(res[i])
        print(x,y)
        draw.ellipse([x-20, y-20, x+20, y+20], fill=(255, 255, 0))
    # draws lines
    for i in range(len(res)):
        x,y = G.get_coordinates(res[i])
        if i+1 < len(res):
            x2, y2 = G.get_coordinates(res[i + 1])
            draw.line([x,y,x2,y2], fill=(0,0,0), width=3)

    img.save('my.png')
    img.show()
