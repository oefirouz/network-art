from PIL import Image, ImageDraw
import pulp
import math
import numpy as np
#from graph import Graph
import collections


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

    ##########################################
    # These are coordinates in test.txt      #
    # 0 72 131                               #
    # 1 125 100                              #
    # 2 125 162                              #
    # 3 425 100                              #
    # 4 372 131                              #
    ##########################################

    with open(filepath) as fp:
        for cnt, line in enumerate(fp):
            s = line.split()
            idx, x, y = s
            coord.append((int(x),int(y)))
            # print("Line {}: {}".format(cnt, line))
            N+=1

    G = {}
    for i in range(N):
        G[i] = (coord[i][0], coord[i][1])

    ################################################################################
    #                                                                              #
    #   THIS IS THE SUBTOUR, cutting group on the left from the right              #
    #   -draws the moats around the control zone                                   #
    ################################################################################

    radii2 = {}
    tour = pulp.LpProblem("tour", pulp.LpMaximize)

    #Creates the variables to be used in objective function
    for i in range(N):
        radii2["r_" + str(i)] = pulp.LpVariable("r_" + str(i), lowBound=0, cat='Continuous')
    radii2["r_Ys"] = pulp.LpVariable("r_Ys", lowBound=0, cat='Continuous')
    radii2["r_Ys2"] = pulp.LpVariable("r_Ys2", lowBound=0, cat='Continuous')

    # Objective function
    tour += 2*radii2["r_0"] + 2*radii2["r_1"] + 2*radii2["r_2"] + 2*radii2["r_3"] + 2*radii2["r_4"] + 2*radii2["r_Ys"] + 2*radii2["r_Ys2"], "Z"

    # Constraints
    for i in range(N):
        for j in range(i + 1, N):
            if (i == 0 and j == 3) or (i == 1 and j == 3) or (i == 2 and j == 3) or (i == 0 and j == 4) or (i == 1 and j == 4) or (i == 2 and j == 4):
                continue
            else:
                tour += radii2["r_" + str(i)] + radii2["r_" + str(j)] <= dist(G[i], G[j])

    tour += (radii2["r_0"] + radii2["r_3"]) +  radii2["r_Ys"] + radii2["r_Ys2"] <= dist(G[0], G[3])
    tour += (radii2["r_1"] + radii2["r_3"]) +  radii2["r_Ys"] + radii2["r_Ys2"]  <= dist(G[1], G[3])
    tour += (radii2["r_2"] + radii2["r_3"]) +  radii2["r_Ys"] + radii2["r_Ys2"] <= dist(G[2], G[3])
    tour += (radii2["r_0"] + radii2["r_4"]) +  radii2["r_Ys"] + radii2["r_Ys2"] <= dist(G[0], G[4])
    tour += (radii2["r_1"] + radii2["r_4"]) +  radii2["r_Ys"] + radii2["r_Ys2"] <= dist(G[1], G[4])
    tour += (radii2["r_2"] + radii2["r_4"]) +  radii2["r_Ys"] + radii2["r_Ys2"]  <= dist(G[2], G[4])

    #Prints in console the function:
    print(tour)

    #Solves the inequalities
    tour.solve()
    pulp.LpStatus[tour.status]

    #Assigns all the radii in a dict so we can draw them
    new_radii2 = {}
    for variable in tour.variables():
        new_radii2[variable.name] = variable.varValue
        print("{} = {}".format(variable.name, variable.varValue))

    for idx, v in enumerate(G):
        if idx < N:
            x, y = G[v]
            if idx < 3:
                moat = new_radii2["r_Ys"]
            else:
                moat = new_radii2["r_Ys2"]

            moat += new_radii2["r_" + str(idx)]

            draw.ellipse([x - moat , y - moat , x + moat , y + moat ], fill=(232, 232, 232))

            draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(0, 0, 0))

    #print("r_Ys", Ys)

    ################################################################################
    #                                                                              #
    #   THIS IS THE MAIN TOUR, creating the control zones                          #
    #                                                                              #
    ################################################################################

    # Draws the control zones
    for idx, v in enumerate(G):
        x, y = G[v]
        temp = new_radii2["r_" + str(idx)]
        draw.ellipse([x - temp, y - temp, x + temp, y + temp], fill=(232, 217, 86))
        draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(0, 0, 0))

    ################################################################################
    #                                                                              #
    #   This creates the route, using int LP, denoted by the black lines
    #                                                                              #
    ################################################################################

    primal = pulp.LpProblem("My LP Problem", pulp.LpMinimize)
    X = {}
    dist_xy = {}

    # Gets the distance (i,j)
    for i in range(N):
        for j in range(i + 1, N):
            dist_xy[(i, j)] = dist(coord[i], coord[j])

    # Sets the variables in dict X, either 1 or 0; tells you whether or not you take the path (i,j)
    for i in range(N):
        for j in range(i + 1, N):
            X[str(i) + "_" + str(j)] = pulp.LpVariable(str(i) + "_" + str(j), lowBound=0, cat='Binary')

    # Objective function:
    primal += pulp.lpSum(X[str(i)+"_"+str(j)] * dist_xy[(i, j)] for i in range(N) for j in range(i+1, N)), "Z"

    # Constraints
    # Creating a temp Object so that it solves it in one line

    for i in range(N):
        temp = pulp.LpAffineExpression()
        for j in range(N):
            if i != j:
                if i < j:
                    temp += pulp.lpSum(X[str(i) + "_" + str(j)])
                else:
                    temp += pulp.lpSum(X[str(j) + "_" + str(i)])
        primal += temp == 2

    # This is what it translates to:
    # primal += X["0_1"] + X["0_2"] + X["0_3"] + X["0_4"] == 2
    # primal += X["0_1"] + X["1_2"] + X["1_3"] + X["1_4"] == 2
    # primal += X["0_2"] + X["1_2"] + X["2_3"] + X["2_4"] == 2
    # primal += X["0_3"] + X["1_3"] + X["2_3"] + X["3_4"] == 2
    # primal += X["0_4"] + X["1_4"] + X["2_4"] + X["3_4"] == 2

    primal.solve()
    for variable in primal.variables():
        X[str(variable.name)] = int(variable.varValue)

    # Connects the path for the final tour
    for path in X:
        if X[path]:
            x_1, y_1 = G[int(path[:1])]
            x_2, y_2 = G[int(path[2:])]
            draw.line([x_1, y_1, x_2, y_2], fill=(0, 0, 0), width=1)


    img.save('my.png')
    img.show()

    """
    ........
    all flights in and out of the city
    #the dual to the primal:
    maximize the size of the circles subject to the circles odont intersect each there
    ...look for the symmetries in the functions

    all those constraints become dual variables for the cities 
    """
