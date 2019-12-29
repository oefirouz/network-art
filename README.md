# Traveling Salesman Problem Visualizer 

This project is a TSP visualizer that uses Integer Linear Programming (branch and bound method) to find the shortest tour that visits each city only once. Typically, the path will not be found in the first iteration, so we need to solve the subtour relaxation by finding relevant constraints, since the number of possible combinations is exponential. We do a DFS to find the subtours and use that information to form new constraints. We repeat this process until a tour is a found.

While the programming is running, it is also solving for the dual of the problem (primal is to minimize the distance, dual is to maximze the width (distance) of the city). It uses the answer of the subtour relaxation of the primal to create new constraints for the dual.

## Algorithm
Let's say we have number of cities n and for two cities, i and j, we let x(i,j) be whether or not we choose to use the city. If the city is used: x(i,j) = 1. If it is not: x(i,j) = 0. To calculate the length of the tour, we calculate the distance of each city and all possible paths from that city and whether or not the city is used. We observe that for every city and its corresponding possible paths, it will sum up to 2 because we have to enter and exit each city exactly once.


![This can be written as:](primal_equation.PNG)
```
Give examples
```


## Resources
http://www.math.uwaterloo.ca/tsp/methods/opt/zone.htm

https://www.epfl.ch/labs/dcg/wp-content/uploads/2018/10/13-TSP.pdf


