import json

from model.vertex import Vertex

class Graph:
    #The Graph itself

    def __init__(self, isDirectioned = False, isValored = False):
        self.order = 0
        self.size = 0
        self.isDirectioned = isDirectioned
        self.isValored = isValored
        self.graph = {}
        
    def addVertex(self, vertex):
        self.graph[vertex.name] = vertex
        self.order+=1
    
    def addEdge(self, edge):
        #atribuindo custo da aresta no objeto de saída do vertice na primeira posição
        
        edge.vertexes[0].exit[edge.vertexes[1].name] = edge.cost
        
        self.graph[edge.vertexes[0].name].exit = edge.vertexes[0].exit
        
        if(self.isDirectioned):
            edge.vertexes[1].entry[edge.vertexes[0].name] = edge.cost
            self.graph[edge.vertexes[1].name].entry = edge.vertexes[1].entry
        else:
            edge.vertexes[1].exit[edge.vertexes[0].name] = edge.cost 
            self.graph[edge.vertexes[1].name].exit = edge.vertexes[1].exit
        
        self.size+=1

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)
    
    def loadGraph(self, graphPath):
        with open(graphPath, 'r') as graphFile:
            graph = json.load(graphFile)
            
            self.order = graph["order"]
            self.size = graph["size"]
            self.isDirectioned = graph['isDirectioned']
            self.isValored = graph['isValored']
            
            for vertexName in graph['graph']:
                vertex = Vertex(vertexName)
                vertex.entry = graph['graph'][vertexName]['entry']
                vertex.exit = graph['graph'][vertexName]['exit']
                
                self.graph[vertexName] = vertex
            
        graphFile.close()
        return self
    
    def saveGraph(self, graphPath):
        with open(graphPath, 'w') as graphFile:
            graphFile.write(self.toJSON())
        graphFile.close()
    
    def listNeighbours(self, vertexName):
        if self.isDirectioned:
            print(f'Vizinhos de entrada de {vertexName}\n\t{self.graph[vertexName].entry}')
            print(f'Vizinhos de saída de {vertexName}\n\t{self.graph[vertexName].exit}')
            return
        print(f'Vizinhos de {vertexName}\n\t{self.graph[vertexName].exit}')
    
    def getDegree(self, vertexName):
        exitDegree = len(list(self.graph[vertexName].exit.keys()))
        textIfDirectioned = ''
        if self.isDirectioned:
            textIfDirectioned = 'saída de '
            entryDegree = len(list(self.graph[vertexName].entry.keys()))
            print(f'Grau de entrada de {vertexName}\n\t{entryDegree}')
        print(f'Grau de {textIfDirectioned}{vertexName}\n\t{exitDegree}')
    
    def areNeighbours(self, vertexName1, vertexName2):
        vertex1ExitNeighbours = list(self.graph[vertexName1].exit.keys())
        vertex1EntryNeighbours = list(self.graph[vertexName1].entry.keys())
        
        result = f'{vertexName1} e {vertexName2} não são vizinhos'
        if vertexName2 in vertex1ExitNeighbours or vertexName2 in vertex1EntryNeighbours:
            result = f'{vertexName1} e {vertexName2} são vizinhos'
        
        print(result)
    
    def highestDegrees(self):
        vertexes = list(self.graph.keys())
        highestExitDegVertexes = {}
        highestExitDegResult = ''
        highestEntryDegVertexes = {}
        highestEntryDegResult = ''
        highestTotalDegVertexes = {}
        highestTotalDegResult = ''
        highestDegNumber = 0
        textIfDirectioned = ''
        
        #se igual concatena, se maior substitui
        #vertice de saida
        for vertex in vertexes:
            if len(self.graph[vertex].exit.keys()) > highestDegNumber:
                highestDegNumber = len(self.graph[vertex].exit.keys())
                highestExitDegVertexes = {vertex: highestDegNumber}
            elif len(self.graph[vertex].exit.keys()) == highestDegNumber:
                highestExitDegVertexes[vertex] = highestDegNumber
                                
        highestExitDegResult = json.dumps(highestExitDegVertexes, default=lambda o: o.__dict__, indent=4)
        
        #vertice de entrada
        if self.isDirectioned:
            textIfDirectioned = 'de saída'
            highestDegNumber = 0
            for vertex in vertexes:
                if len(self.graph[vertex].entry.keys()) > highestDegNumber:
                    highestDegNumber = len(self.graph[vertex].entry.keys())
                    highestEntryDegVertexes = {vertex: highestDegNumber}
                elif len(self.graph[vertex].entry.keys()) == highestDegNumber:
                    highestEntryDegVertexes[vertex] = highestDegNumber
            highestEntryDegResult = json.dumps(highestEntryDegVertexes, default=lambda o: o.__dict__, indent=4)
            print(f'Maior grau de entrada:', highestEntryDegResult)
                
        print(f'Maior grau {textIfDirectioned}:', highestExitDegResult)
        
        #Grau total
        if self.isDirectioned:
            highestDegNumber = 0
            for vertex in vertexes:
                if len(self.graph[vertex].entry.keys()) + len(self.graph[vertex].exit.keys()) > highestDegNumber:
                    highestDegNumber = len(self.graph[vertex].entry.keys()) + len(self.graph[vertex].exit.keys())
                    highestTotalDegVertexes = {vertex: highestDegNumber}
                elif len(self.graph[vertex].entry.keys()) + len(self.graph[vertex].exit.keys()) == highestDegNumber:
                    highestTotalDegVertexes[vertex] = highestDegNumber
            highestTotalDegResult = json.dumps(highestTotalDegVertexes, default=lambda o: o.__dict__, indent=4)
            print('Maior grau total:', highestTotalDegResult)

    def shortestPath(self, vertexName1, vertexName2):
        #init Djikstra
        djikstra = {}
        djikstraPath = []
        djikstraContinue = True
        
        for vertex in list(self.graph.keys()):
            if vertex == vertexName1:
                djikstra[vertex] = {
                    'cost': 0,
                    'from': '',
                    'isOpen': True
                }
            else:
                djikstra[vertex] = {
                    'cost': float('inf'),
                    'from': '',
                    'isOpen': True
                }
        
        #Agora começa a brincadeira
        while(djikstraContinue):
            djikstraContinue = False
            vertexes = list(djikstra.keys())
            openVertexes = {}
            #verificando se tem vertices abertos
            for vertex in vertexes:
                if djikstra[vertex]['isOpen']:
                    djikstraContinue = True
                    openVertexes[vertex] = djikstra[vertex]
            
            #selecionando a aresta de menor custo
            if len(openVertexes) > 0:
                leastCostVertex = None
                minCost = float('inf')
                for vertex in openVertexes:
                    if djikstra[vertex]['cost'] < minCost:
                        minCost = djikstra[vertex]['cost']
                        leastCostVertex = self.graph[vertex]

                djikstra[leastCostVertex.name]['isOpen'] = False
                edgesToRelax = leastCostVertex.exit
                vertexCost = djikstra[leastCostVertex.name]['cost']
                
                #Relaxando as arestas
                for exitVertex in edgesToRelax:
                    if edgesToRelax[exitVertex] + vertexCost < djikstra[exitVertex]['cost']:
                        djikstra[exitVertex]['cost'] = edgesToRelax[exitVertex]
                        djikstra[exitVertex]['from'] = leastCostVertex.name
        
        vertex = vertexName2
        djikstraPath.append(vertexName2)
        while djikstra[vertex]['from'] != '':
            djikstraPath.append(djikstra[vertex]['from'])
            vertex = djikstra[vertex]['from']
        
        djikstraPath.reverse()
        
        shortestPath = ''
        for vertex in djikstraPath:
            arrow = '->'
            if vertex == djikstraPath[-1]:
                arrow = ''
            shortestPath += f'{vertex}{arrow}'
            
        print('Caminho:', shortestPath)
        print('Custo:', djikstra[djikstraPath[-1]]['cost'])