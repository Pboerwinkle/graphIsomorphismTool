This readme is intended to be read in plain monospace text.

This tool is used to make graphs! Graphs as in: https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)
You will need python3, pygame, and numpy
Run with `python3 graphMaker.py`

GUI:
_________________________________________
|1|5                 |9                 |
|2|6                 |10                |
| |    ________      |    o             |
| |   |__   7  |     |                  |
| |      |__   |     |       11     o   |
| |         |__|     |                  |
| |                  |    o             |
|3|                  |                  |
|4|________ 8 _______|__________________|

1. add a graph to your set of graphs
2. select which graph you want to edit
3. load a set of graphs
   - in the terminal, type the path to the graph set from the 'graphSets' folder
4. save your set of graphs
   - in the terminal, type the path to the graph set from the 'graphSets' folder
5. add an edge to the current graph
6. remove an edge from the current graph
7. matrix representation of the current graph
   - move the circles to change the endpoints of the edges
   - when you hold click on an edge, it will show all of the locations you can move the edge to to keep the graph isomorphic.
   - note that you can move edges to positions below the main diagonal, but since these are undirected graphs, they are symmetric, so the region below the main diagonal is a reflection of the region above the main diagonal.
8. remove the current graph from your set of graphs
9. add a vertex to the current graph
10. remove a vertex from the current graph
11. graphical representation of the graph (wait... GRAPHical?)
