from model.graph import Graph
from model.edge import Edge
from model.vertex import Vertex

graphObj = None

#carregar arquivo
def load(filePath):
    graphObj = Graph()
    return graphObj.loadGraph(filePath)

#salvar arquivo
def save(graph, filePath):
    graph.saveGraph(filePath)
    print(f'Salvo com sucesso em {filePath}')

def checkVertex(vertexName, vertexes):
    if vertexName in vertexes:
        return True
    else:
        print('Não existe vértice com esse nome')
        return False

#Menu
print('Bem vindo ao Graph Builder')
willLoad = input('Você deseja carregar um grafo salvo?(y/N)')
if willLoad == 'y':
    filePath = input('Informe o caminho para o arquivo (Formato: caminho/para/arquivo.json) (Apenas aperte enter para abortar)')
    #filePath = 'graphs/av1.json'
    if filePath != '':
        graphObj = load(filePath)
    else:
        print('Carregamento abortado')
    
if graphObj is None:
    isDirectioned = input('Você pretende usar grafo direcionado?(y/N)')
    isValored = input('Você pretende usar grafo valorado?(y/N)')
    graphObj = Graph(isDirectioned == 'y', isValored == 'y')

print(graphObj.toJSON())
MENUPRINCIPAL = '1) Adicionar vértice\n2) Adicionar aresta\n3) Salvar grafo\n4) Adjacentes de um vértice\n5) Grau de vértice\n6) Checar adjacência de dois vértices\n7) Checar maiores graus\n8) Obter menor caminho(Djikstra)\n9) Mostrar Grafo\n0) Sair\n'
op = int(input(MENUPRINCIPAL))

while(op != 0):
    vertexes = list(graphObj.graph.keys())
    if op == 1:
        vertexName = input('Nome do vertice: ')
        if vertexName not in vertexes:
            vertex = Vertex(vertexName)
            graphObj.addVertex(vertex)
        else:
            print('Já existe vértice com esse nome')
    elif op == 2:
        if len(vertexes) < 2:
            print('Não há vertices suficientes para criar uma aresta')
        else:
            vertexName1 = input('Escolha o primeiro vértice:')
            if(vertexName1 in vertexes):
                vertexName2 = input('Escolha o segundo vértice:')
                if(vertexName2 in vertexes):
                    if vertexName1 != vertexName2:
                        define = ''
                        if vertexName2 in graphObj.graph[vertexName1].exit :
                            define = input('Esta aresta já está definida, deseja sobrescrever?(y/N)')
                        else:
                            define = 'y'
                        if define == 'y':
                            if graphObj.isValored:
                                cost = int(input('Defina um custo para a aresta: (digite 0 ou menos para uma aresta não valorada)'))
                                if cost < 1:
                                    edge = Edge((graphObj.graph[vertexName1], graphObj.graph[vertexName2]))
                                else:
                                    edge = Edge((graphObj.graph[vertexName1], graphObj.graph[vertexName2]), cost)
                            else:
                                edge = Edge((graphObj.graph[vertexName1], graphObj.graph[vertexName2]))
                            graphObj.addEdge(edge)
                    else:
                        print('Não é possível criar laços')
                else:
                    print('Não existe vértice com esse nome')
            else:
                print('Não existe vértice com esse nome')
    elif op == 3:
        filePath = input('Informe o caminho para o arquivo (Formato: caminho/para/arquivo.json) (Apenas aperte enter para abortar)')
        if filePath != '':
            save(graphObj, filePath)
        else:
            print('Salvamento abortado')
    elif op == 4:
        vertexName = input('Nome do vertice: ')
        if checkVertex(vertexName, vertexes):
            graphObj.listNeighbours(vertexName)
    elif op == 5:
        vertexName = input('Nome do vertice: ')
        if checkVertex(vertexName, vertexes):
            graphObj.getDegree(vertexName)
    elif op == 6:
        if len(vertexes) < 2:
            print('Não há vertices suficientes para essa opção')
        else:
            vertexName1 = input('Nome do primeiro vértice: ')
            if checkVertex(vertexName1, vertexes):
                vertexName2 = input('Nome do segundo vértice: ')
                if checkVertex(vertexName2, vertexes):
                    graphObj.areNeighbours(vertexName1, vertexName2)
    elif op == 7:
        graphObj.highestDegrees()
    elif op == 8:
        #Djikstra
        if len(vertexes) < 2:
            print('Não há vertices suficientes para essa opção')
        else:
            vertexName1 = input('Nome do primeiro vértice: ')
            if checkVertex(vertexName1, vertexes):
                vertexName2 = input('Nome do segundo vértice: ')
                if checkVertex(vertexName2, vertexes):
                    #Djikstra
                    graphObj.shortestPath(vertexName1, vertexName2)
    elif op == 9:
        print(graphObj.toJSON())
    else:
        print('Opção inválida')
    
    op = int(input(MENUPRINCIPAL))

print('Obrigado por usar o Graph Builder')