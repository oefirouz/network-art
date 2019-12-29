# Traveling Salesman Problem Visualizer 

This project is a TSP visualizer that uses Integer Linear Programming (branch and bound method) to find the shortest tour that visits each city only once. Typically, the path will not be found in the first iteration, so we need to solve the subtour relaxation by finding relevant constraints, since the number of possible combinations is exponential. We do a DFS to find the subtours and use that information to form new constraints. We repeat this process until a tour is a found.

While the programming is running, it is also solving for the dual of the problem (primal is to minimize the distance, dual is to maximze the width (distance) of the city). It uses the answer of the subtour relaxation of the primal to create new constraints for the dual.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

## Resources
http://www.math.uwaterloo.ca/tsp/methods/opt/zone.htm
https://www.epfl.ch/labs/dcg/wp-content/uploads/2018/10/13-TSP.pdf


