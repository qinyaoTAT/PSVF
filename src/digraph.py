# -*- coding:utf-8 -*-
import graphviz
import logging


class Digraph:
    def __init__(self):
        self.graph = {}
        # 记录行号信息
        self.graph_record = {}
        self.lineno = 0

    def add_vertex(self, value):
        if not value:
            return
        if value not in self.graph and isinstance(value, str):
            self.graph[value] = []
            self.graph_record[value] = set()
            self.graph_record[value].add(self.lineno)

    def del_vertex(self, value):
        if not value:
            return
        if value in self.graph and isinstance(value, str):
            self.graph.pop(value)
            self.graph_record.pop(value)

    def add_edge(self, vertex_out, vertex_in):
        if not vertex_out or not vertex_in:
            return
        if ':' in vertex_out or ':' in vertex_in:
            return
        if vertex_in not in self.graph:
            self.graph[vertex_in] = []
            self.graph_record[vertex_in] = set()
            self.graph_record[vertex_in].add(self.lineno)
        if vertex_out not in self.graph:
            self.graph[vertex_out] = []
            self.graph_record[vertex_out] = set()
            self.graph_record[vertex_in].add(self.lineno)
        if vertex_in not in self.graph[vertex_out]:
            self.graph[vertex_out].append(vertex_in)

    def add_mul_vertex_edge(self, *args, **kwargs):
        pass

    def get_lineno(self, value):
        node_name, lineno = value.split('##')
        return node_name, lineno

    def generate(self, output, project_name='psvf'):
        dot = graphviz.Digraph(project_name, comment='generate project value flow graph.', node_attr={'color': 'lightblue2', 'style': 'filled'})
        dot.format = 'pdf'
        for i in self.graph:
            if self.graph[i]:
                if self.graph_record[i]:
                    dot.node(i, i + str(self.graph_record[i]))
                else:
                    dot.node(i)
                for j in self.graph[i]:
                    dot.edge(str(i), str(j))
        logging.info('start write visualization file...')
        dot.render(directory=output).replace('\\', '/')


