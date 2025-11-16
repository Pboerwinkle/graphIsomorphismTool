import math as m
import numpy as np
import pygame
import pygame.gfxdraw
import colorsys
import json
pygame.init()
screenSize = (800, 510)
screen = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock() 
framerate=30
numberImgs=pygame.image.load("characters.png")
def drawNumber(number, position):
    screen.blit(numberImgs, position, (10*number, 0, 10, 16))

def getGraphPos(graph, vertex, change, shape):
    if shape == 0:
        return [round((3*screenSize[0]+30)//4+((screenSize[0]-30)*0.15+change)*m.cos(2*m.pi*vertex/Graphs[graph].vertices)), round(screenSize[1]//2+((screenSize[0]-30)*0.15+change)*m.sin(2*m.pi*vertex/Graphs[graph].vertices))]
    else:
        return [round((3*screenSize[0]+30)//4+((screenSize[0]-30)*0.15)*m.cos(2*m.pi*vertex/Graphs[graph].vertices+change)), round(screenSize[1]//2+((screenSize[0]-30)*0.15)*m.sin(2*m.pi*vertex/Graphs[graph].vertices+change))]
def getMatrixPos(vertices, x, y):
    return [(screenSize[0]+3*30)//4 - vertices*40//2 + y*40 + 20, screenSize[1]//2 - vertices*40//2 + x*40 + 20]
def getEdgeColor(graph, edge, value=1):
    return 255*np.array(colorsys.hsv_to_rgb(edge/len(Graphs[graph].edges), 1, value))

def compressGraph(graph):### Compress graph, ex: [[2,3], [3,3], [3,4]] -> [[0,1], [1,1], [1,2]]
    checkVars = []
    newEdges = []
    for edge in range(len(graph)):
        newEdge = []
        for element in range(len(graph[edge])):
            foundVar = False
            for var in range(len(checkVars)):
                if graph[edge][element] == checkVars[var]:
                    newEdge.append(var)
                    foundVar = True
                    break
            if not foundVar:
                newEdge.append(len(checkVars))
                checkVars.append(graph[edge][element])
        newEdges.append(newEdge)
    return newEdges, len(checkVars)

def compareGraphs(graph1, graph2):
    relationsLeft = [edge.copy() for edge in graph2]
    for edge in graph1:
        foundEdge=False
        i=0
        for relation in range(len(relationsLeft)):
            if compareEdges(relationsLeft[relation], edge):
                foundEdge=True
                i=relation
                break
        if foundEdge:
            relationsLeft.pop(i)
        else:
            return False
    return True

def genPermutations(items):
    permutations=[]
    for i in range(m.factorial(items)):
        thisPerm=[]
        allValues=[k for k in range(items)]
        for j in range(items):
            index=i//m.factorial(items-1-j)%(items-j)
            thisPerm.append(allValues[index])
            allValues.pop(index)
        permutations.append(thisPerm)
    return permutations

def reformatGraph(graph, mapping):
    newGraph = []
    for edge in graph:
        newEdge=[]
        for component in edge:
            newEdge.append(mapping[component])
        newGraph.append(newEdge)
    return newGraph

def compareEdges(edge1, edge2):
    if np.array_equal(edge1, edge2) or np.array_equal(np.flip(edge1), edge2):
        return True
    else:
        return False

class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        self.multiplicity = []
        self.computeMultiplicity()

    def checkValidPos(self, edgeIndex, pos):
        
        newEdges = [[self.edges[row][i] for i in range(2)] for row in range(len(self.edges))]
        newEdges[edgeIndex] = pos

        newEdges, varNum = compressGraph(newEdges)
        oldEdges, x = compressGraph(self.edges)

        ### Check if the compressed form matches the original
        varMappings = genPermutations(varNum)#not polynomial time :'(
        for mapping in varMappings:
            if compareGraphs(oldEdges, reformatGraph(newEdges, mapping)):
                return True
        return False

    def computeMultiplicity(self):
        self.multiplicity = np.zeros(len(self.edges))
        for edge1 in range(len(self.edges)):
            for edge2 in range(edge1+1, len(self.edges)):
                if compareEdges(self.edges[edge1], self.edges[edge2]):
                    self.multiplicity[edge2]+=1

    def getAllValidPos(self, edgeIndex):
        validPos = []
        for i in range(self.vertices):
            for j in range(i, self.vertices):
                valid=self.checkValidPos(edgeIndex, (i, j))
                if valid:
                    validPos.append([i, j])
        return validPos

Graphs = [Graph(4, [[0, 0]])]
scrollPos = 0
graphSelected = 0
edgeSelected = -1
cellHovered = [0, 0]

done = False
while not done:
    clock.tick(framerate)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done=True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done=True

        if event.type == pygame.MOUSEMOTION:
            if graphSelected != -1:
                cellHovered = np.flip(np.array(event.pos)-getMatrixPos(Graphs[graphSelected].vertices, 0, 0)+20)//40
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                scrollPos = max(0, scrollPos-1)
            if event.button == 5:
                scrollPos = max(0, min(len(Graphs)-(screenSize[1]//30-3), scrollPos+1))
            if event.button == 1:
                ### Interacting with graph panel
                if event.pos[0] < 30 or graphSelected == -1:
                    selection = event.pos[1]//30
                    ### Add graph
                    if selection == 0:
                        Graphs.append(Graph(4, [[0, 0]]))
                    ### Save graphs
                    elif selection == screenSize[1]//30-1:
                        path="graphSets/"+input("Save to: graphSets/")
                        toSave = [[graph.vertices, graph.edges] for graph in Graphs]
                        toSave = json.dumps(toSave)
                        saveFile = open(path, "w")
                        saveFile.write(toSave)
                        saveFile.close()
                    ### Load graphs
                    elif selection == screenSize[1]//30-2:
                        path="graphSets/"+input("Load from: graphSets/")
                        loadFile = open(path, "r")
                        toLoad = json.loads(loadFile.read())
                        loadFile.close()
                        for graph in toLoad:
                            Graphs.append(Graph(graph[0], graph[1]))
                    ### Select graph
                    else:
                        selection = min(selection, len(Graphs))
                        graphSelected = selection-1+scrollPos
                ### Interacting with matrix area
                elif event.pos[0] < (screenSize[0]+30)//2:
                    ### Add edge
                    if event.pos[1] < 22:
                        Graphs[graphSelected].edges.append([0, 0])
                        Graphs[graphSelected].computeMultiplicity()
                    ### Remove edge
                    elif event.pos[1] < 44:
                        if len(Graphs[graphSelected].edges) > 0:
                            Graphs[graphSelected].edges.pop(-1)
                            Graphs[graphSelected].computeMultiplicity()
                    ### Interact with edges
                    elif event.pos[1] < screenSize[1]-24:
                        for edge in range(len(Graphs[graphSelected].edges)):
                            if np.array_equal(Graphs[graphSelected].edges[edge], cellHovered):
                                edgeSelected = edge
                                break
                    ### Remove graph
                    else:
                        Graphs.pop(graphSelected)
                        if graphSelected == len(Graphs):
                            graphSelected -= 1
                        scrollPos = max(0, min(len(Graphs)-(screenSize[1]//30-3), scrollPos+1))
                ### Interacting with graph area
                else:
                    ### Add vertex
                    if event.pos[1] < 22:
                        Graphs[graphSelected].vertices+=1
                    ### Remove vertex
                    elif event.pos[1] < 44 and Graphs[graphSelected].vertices>1:
                        Graphs[graphSelected].vertices-=1
                        for edge in range(len(Graphs[graphSelected].edges)):
                            Graphs[graphSelected].edges[edge] = [max(min(Graphs[graphSelected].edges[edge][0], Graphs[graphSelected].vertices-1), 0), max(min(Graphs[graphSelected].edges[edge][1], Graphs[graphSelected].vertices-1), 0)]
                        Graphs[graphSelected].computeMultiplicity()
                        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if edgeSelected != -1:
                    dropCell = [max(min(cellHovered[0], Graphs[graphSelected].vertices-1), 0), max(min(cellHovered[1], Graphs[graphSelected].vertices-1), 0)]
                    Graphs[graphSelected].edges[edgeSelected] = [int(dropCell[0]), int(dropCell[1])]
                    Graphs[graphSelected].computeMultiplicity()
                edgeSelected = -1

    ### 


    screen.fill((0, 0, 0))
    pygame.gfxdraw.box(screen, (0, 0, 30, screenSize[1]), (40, 40, 40))
    pygame.gfxdraw.box(screen, (0, 30*(graphSelected+1-scrollPos), 30, 30), (0, 0, 0))
    pygame.gfxdraw.box(screen, ((screenSize[0]+30)//2-1, 0, 2, screenSize[1]), (255, 255, 255))
    drawNumber(10, (10, 7))
    for i in range(scrollPos, min(scrollPos+screenSize[1]//30-3, len(Graphs))):
        for char in range(len(str(i))):
            drawNumber(int(str(i)[char]), (16-6*len(str(i))+char*11, (i-scrollPos+1)*30+7))
    drawNumber(12, (10, screenSize[1]-53))
    drawNumber(13, (10, screenSize[1]-23))

    if graphSelected == -1:
        pygame.display.flip()
        continue

    ### Draw valid positions
    if edgeSelected != -1:
        validPos = Graphs[graphSelected].getAllValidPos(edgeSelected)
        for pos in validPos:
            pygame.gfxdraw.box(screen, (*np.array(getMatrixPos(Graphs[graphSelected].vertices, pos[0], pos[1]))-20, 40, 40), getEdgeColor(graphSelected, edgeSelected))

    ### Draw matrix base
    for i in range(Graphs[graphSelected].vertices):
        for j in range(i, Graphs[graphSelected].vertices):
            pygame.gfxdraw.filled_circle(screen, *getMatrixPos(Graphs[graphSelected].vertices, i, j), 20, (100, 100, 100))

    ### Draw relations
    for edge in range(len(Graphs[graphSelected].edges)):
        color = getEdgeColor(graphSelected, edge)
        #On matrix
        if edge != edgeSelected:
            pygame.gfxdraw.filled_circle(screen, *getMatrixPos(Graphs[graphSelected].vertices, Graphs[graphSelected].edges[edge][0], Graphs[graphSelected].edges[edge][1]), 15, color)

        #Numerically
        pygame.gfxdraw.box(screen, (36+edge*20, 0, 18, 44), getEdgeColor(graphSelected, edge, value=0.5))
        drawNumber(Graphs[graphSelected].edges[edge][0], (40+edge*20, 4))
        drawNumber(Graphs[graphSelected].edges[edge][1], (40+edge*20, 24))

        #On graph
        if Graphs[graphSelected].edges[edge][0] == Graphs[graphSelected].edges[edge][1]:
            pygame.draw.circle(screen, color, getGraphPos(graphSelected, Graphs[graphSelected].edges[edge][0], 20+Graphs[graphSelected].multiplicity[edge]*5, 0), 20+Graphs[graphSelected].multiplicity[edge]*5, width=2)
        else:
            pygame.draw.line(screen, color, getGraphPos(graphSelected, Graphs[graphSelected].edges[edge][0], Graphs[graphSelected].multiplicity[edge]/15, 1), getGraphPos(graphSelected, Graphs[graphSelected].edges[edge][1], -Graphs[graphSelected].multiplicity[edge]/15, 1), width=2)

    drawNumber(10, (40+len(Graphs[graphSelected].edges)*20, 4))
    drawNumber(11, (40+len(Graphs[graphSelected].edges)*20, 24))
    drawNumber(10, ((screenSize[0]+30)//2+10, 4))
    drawNumber(11, ((screenSize[0]+30)//2+10, 24))
    pygame.gfxdraw.box(screen, (40, screenSize[1]-24, (screenSize[0]-30)//2-20, 24), (40, 40, 40))
    drawNumber(11, ((screenSize[0]+90)//4-5, screenSize[1]-20))

    ### Draw held edge, and graph outcomes
    if edgeSelected != -1:
        pygame.gfxdraw.filled_circle(screen, *getMatrixPos(Graphs[graphSelected].vertices, cellHovered[0], cellHovered[1]), 15, getEdgeColor(graphSelected, edgeSelected, value=0.5))
        for pos in validPos:
            if pos[0] == pos[1]:
                pygame.draw.circle(screen, getEdgeColor(graphSelected, edgeSelected, value=0.5), getGraphPos(graphSelected, pos[0], 20, 0), 20, width=2)
            else:
                pygame.draw.line(screen, getEdgeColor(graphSelected, edgeSelected, value=0.5), getGraphPos(graphSelected, pos[0], 0, 1), getGraphPos(graphSelected, pos[1], 0, 1), width=2)

    ### Draw graph base
    for i in range(Graphs[graphSelected].vertices):
        pygame.gfxdraw.filled_circle(screen, *getGraphPos(graphSelected, i, 0, 0), 10, (255, 255, 255))

    pygame.display.flip()
pygame.quit()