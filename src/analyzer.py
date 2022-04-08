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
            self.bfs(vertex)

    def bfs(self, vertex):
        que = queue.Queue()
        que.put(vertex)
        self.visited_vertex = set()
        while not que.empty():
            v = que.get()
            print(v)
            for i in self.graph[v]:
                if i not in self.visited_vertex:
                    self.visited_vertex.add(i)
                    que.put(i)




