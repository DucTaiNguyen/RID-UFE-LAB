import numpy as np

class KnowledgeGraph:

    def __init__(self):
        self.nodes = set()
        self.edges = {}

    def add_node(self, name):
        self.nodes.add(name)

    def add_edge(self, a, b, weight):
        # convert tuple key → string key (JSON-safe)
        key = f"{a}__{b}"
        self.edges[key] = float(weight)

    def summary(self):
        return {
            "nodes": list(self.nodes),
            "edges": self.edges
        }
