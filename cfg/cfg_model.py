import networkx as nx

class cfg:
    def __init__(self, var):
        self.graph = nx.DiGraph()
        self.var = var
