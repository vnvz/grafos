class Edge :
    # Edge of a Graph

    def __init__(self, pair_of_vertexes, cost = 0):
        
        self.vertexes = pair_of_vertexes # (vertex1, vertex2)
        self.cost = cost