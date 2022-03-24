# -*- coding:utf-8 -*-

class Digraph:
    def __init__(self, num):
        self.graph = {}

    def add_vertex(self, value):
        if not value:
            return
        if value not in self.graph and isinstance(value, str):
            self.graph[value] = []

    def add_edge(self, vertex_out, vertex_in):
        if not vertex_out:
            return
        if vertex_out not in self.graph:
            self.graph[vertex_out] = []
        else:
            self.graph[vertex_out].append(vertex_in)

    def add_vertex_edge(self, *args, **kwargs):
        pass
