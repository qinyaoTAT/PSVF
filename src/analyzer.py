# -*- coding:utf-8 -*-
import json
import queue

from src import rules

class DFS:
    def __init__(self, graph):
        self.graph = graph
        self.start_vertex = set()
        self.trace = []
        self.errors = []
        self.visited_vertex = set()
        self.get_start_vertex()

    def get_start_vertex(self):
        self.start_vertex = set(self.graph.keys())
        sub_vertext_set = set()
        for vertex in self.graph:
            sub_vertext_set |= set(self.graph[vertex])
        for i in sub_vertext_set:
            if i in self.start_vertex:
                self.start_vertex.remove(i)

    def analyze(self):
        for vertex in self.start_vertex:
            self.dfs(vertex)

    def dfs(self, vertex):
        for i in self.graph[vertex]:
            if i not in self.visited_vertex:
                self.visited_vertex.add(i)
                print(i)
                self.dfs(i)




