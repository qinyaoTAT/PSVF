# -*- coding:utf-8 -*-
import graphviz

class Digraph:
    def __init__(self):
        self.graph = {}
        self.lineno = 0

    def add_vertex(self, value):
        if not value:
            return
        if value not in self.graph and isinstance(value, str):
            value += '##' + str(self.lineno)
            self.graph[value] = []

    def del_vertex(self, value):
        if not value:
            return
        if value in self.graph and isinstance(value, str):
            value += '##' + str(self.lineno)
            self.graph.pop(value)

    def add_edge(self, vertex_out, vertex_in):
        if not vertex_out or not vertex_in:
            return
        vertex_out += '##' + str(self.lineno)
        vertex_in += '##' + str(self.lineno)
        if vertex_in not in self.graph:
            self.graph[vertex_in] = []
        if vertex_out not in self.graph:
            self.graph[vertex_out] = []
        self.graph[vertex_in].append(vertex_out)

    def add_mul_vertex_edge(self, *args, **kwargs):
        pass

    def get_lineno(self, value):
        node_name, lineno = value.split('##')


    def write(self, fmt='pdf', module_name='psvf'):
        dot = graphviz.Digraph(module_name, comment=module_name, node_attr={'color': 'lightblue2', 'style': 'filled'})
        dot.format = fmt
        for i in self.graph:
            if self.graph[i]:
                dot.node(i, i + '')
                for j in self.graph[i]:
                    dot.edge(j, i)
        dot.render(directory='output').replace('\\', '/')


