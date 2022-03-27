# -*- coding:utf-8 -*-

class Digraph:
    def __init__(self):
        self.graph = {}

    def add_vertex(self, value):
        if not value:
            return
        if value not in self.graph and isinstance(value, str):
            self.graph[value] = []

    def del_vertex(self, value):
        if not value:
            return
        if value in self.graph and isinstance(value, str):
            self.graph.pop(value)

    def add_edge(self, vertex_out, vertex_in):
        if not vertex_out:
            return
        if vertex_in not in self.graph:
            self.graph[vertex_in] = []
        self.graph[vertex_in].append(vertex_out)

    def add_vertex_edge(self, *args, **kwargs):
        pass
