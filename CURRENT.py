from PIL import Image, ImageDraw
import pulp
import math
import numpy as np
#from graph import Graph
import collections


"""
These are the coordinates in test.txt:
(72 131)
(125 100)
(125 162)
(372 131)
(425 100)
"""
if __name__ == "__main__":
    def dist(p1, p2):  # takes tuple
        distance = math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))
        return distance

    w, h = 1024, 512
    data = np.zeros((h, w, 3), dtype=np.uint8)
    for i in range(0, 500):
        for j in range(0, 1024):
            data[i, j] = [100,100,100]

    img = Image.fromarray(data, 'RGB')
    draw = ImageDraw.Draw(img)

    #this is basic graph
    N = 0
    coord = []
    filepath = "tsplib/test.txt"
    with open(filepath) as fp:
        for cnt, line in enumerate(fp):
            s = line.split()
            idx, x, y = s
            coord.append((int(x),int(y)))
            #print(x, y)
            # print("Line {}: {}".format(cnt, line))
            N+=1

    print(coord)
    G = {}
    for i in range(N):
        G[i] = (coord[i][0], coord[i][1])

        ############################
        #
        #       THIS IS THE SUBTOUR CUT!!!!
        #
        #

    radii2 = {}
    subtour = pulp.LpProblem("subtour", pulp.LpMaximize)

    for i in range(N):
        radii2["r_" + str(i)] = pulp.LpVariable("r_" + str(i), lowBound=0, cat='Continuous')

    radii2["r_Y"] = pulp.LpVariable("r_Y", lowBound=0, cat='Continuous')

    # Objective function

    subtour += 2*radii2["r_0"] + 2*radii2["r_1"] + 2*radii2["r_2"] + 2*radii2["r_3"] + 2*radii2["r_4"] + 2*radii2["r_Y"], "Z"

    # Constraints
    for i in range(N):
        for j in range(i + 1, N):
            print(i, j)
            if (i == 0 and j == 3) or (i == 1 and j == 3) or (i == 2 and j == 3) or (i == 0 and j == 4) or (i == 1 and j == 4) or (i == 2 and j == 4):
                continue
            else:
                subtour += radii2["r_" + str(i)] + radii2["r_" + str(j)] <= dist(G[i], G[j])

    subtour += (radii2["r_0"] + radii2["r_3"]) +  radii2["r_Y"]*2 <= dist(G[0], G[3])
    subtour += (radii2["r_1"] + radii2["r_3"]) +  radii2["r_Y"]*2 <= dist(G[1], G[3])
    subtour += (radii2["r_2"] + radii2["r_3"]) +  radii2["r_Y"]*2 <= dist(G[2], G[3])
    subtour += (radii2["r_0"] + radii2["r_4"]) +  radii2["r_Y"]*2 <= dist(G[0], G[4])
    subtour += (radii2["r_1"] + radii2["r_4"]) +  radii2["r_Y"]*2 <= dist(G[1], G[4])
    subtour += (radii2["r_2"] + radii2["r_4"]) + radii2["r_Y"]*2 <= dist(G[2], G[4])


    subtour.solve()
    pulp.LpStatus[subtour.status]
    new_radii2 = {}

    for variable in subtour.variables():
        new_radii2[variable.name] = variable.varValue

    Ys = new_radii2["r_Y"]
    for idx, v in enumerate(G):
        if idx < 5:
            x, y = G[v]
            temp = new_radii2["r_" + str(idx)]
            draw.ellipse([x - Ys , y - Ys , x + Ys , y + Ys ], fill=(232, 232, 232))
            draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(0, 0, 0))

    print("r_Y", Ys)

    #############################
    #this is PRIMAL
    radii = {}
    test = pulp.LpProblem("My LP Problem", pulp.LpMaximize)

    for i in range(N):
        radii["r_" + str(i)] = pulp.LpVariable("r_" + str(i), lowBound=0, cat='Continuous')

    # Objective function
    test += pulp.lpSum(2*radii["r_" + str(i)] for i in range(N)), "Z"
    # Constraints
    for i in range(N):
        for j in range(i + 1, N):
            print(i, j)
            test += radii["r_" + str(i)] + radii["r_" + str(j)] <= dist(G[i],
                                                                                 G[j])

    test.solve()
    pulp.LpStatus[test.status]
    new_radii = {}

    for variable in test.variables():
        new_radii[variable.name] = variable.varValue

    for idx, v in enumerate(G):
        x, y = G[v]
        temp = new_radii["r_" + str(idx)]
        draw.ellipse([x - temp, y - temp, x + temp, y + temp], fill=(232, 217, 86))
        draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(0, 0, 0))

    ############################
    ############################
    #############################
    #############################
    # this draws the TOUR, not the radii

    primal = pulp.LpProblem("My LP Problem", pulp.LpMinimize)
    X = {}
    dist_xy = {}

    # gets the distance (i,j) from graph
    for i in range(N):
        for j in range(i + 1, N):
            dist_xy[(i, j)] = dist(coord[i], coord[j])

    # sets the variables in dict X, either 1 or 0
    for i in range(N):
        for j in range(i + 1, N):
            X[str(i) + "_" + str(j)] = pulp.LpVariable(str(i) + "_" + str(j), lowBound=0, cat='Binary')

    print("xxxx", X)
    # objective function:

    primal += pulp.lpSum(X[str(i)+"_"+str(j)] * dist_xy[(i, j)] for i in range(N) for j in range(i+1, N)), "Z"


    #constraints
    for i in range(N):
        temp = pulp.LpAffineExpression()
        for j in range(N):
            if i != j:
                if i < j:
                    temp += pulp.lpSum(X[str(i) + "_" + str(j)])
                else:
                    temp += pulp.lpSum(X[str(j) + "_" + str(i)])
        primal += temp == 2


    primal.solve()
    pulp.LpStatus[primal.status]
    for variable in primal.variables():
        X[str(variable.name)] = int(variable.varValue)

    for path in X:
        if X[path]:
            x_1, y_1 = G[int(path[:1])]
            x_2, y_2 = G[int(path[2:])]
            draw.line([x_1, y_1, x_2, y_2], fill=(0, 0, 0), width=1)

 #draws circles: coordinates are center of circle
    img.save('my.png')
    img.show()
