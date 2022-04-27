# -*- coding:utf-8 -*-
import graphviz
import logging


class Digraph:
    def __init__(self):
        # graph 的节点值不要手动修改
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
            self.add_vertex(vertex_in)
        if vertex_out not in self.graph:
            self.add_vertex(vertex_out)
        if vertex_in not in self.graph[vertex_out]:
            self.graph[vertex_out].append(vertex_in)

    def add_mul_vertex_edge(self, *args, **kwargs):
        pass

    def get_lineno(self, value):
        node_name, lineno = value.split('##')
        return node_name, lineno

    def generate(self, output, errors, project_name='psvf'):
        errors_transfer_set = set()
        errors_source_sink_set = set()
        for i in errors:
            for j in i:
                if j == i[0] or j == i[-1]:
                    errors_source_sink_set.add(j)
                else:
                    errors_transfer_set.add(j)
        dot = graphviz.Digraph(project_name, comment='generate project value flow graph.', node_attr={'color': 'lightblue2', 'style': 'filled'})
        dot.format = 'pdf'
        for i in self.graph:
            if self.graph[i]:
                if self.graph_record[i]:
                    if i in errors_source_sink_set:
                        dot.node(i, i + str(self.graph_record[i]), color='red')
                    else:
                        dot.node(i, i + str(self.graph_record[i]))
                else:
                    dot.node(i)
                for j in self.graph[i]:
                    if (j in errors_transfer_set and i in errors_transfer_set) or \
                            (j in errors_transfer_set and i in errors_source_sink_set) or \
                            (j in errors_source_sink_set and i in errors_transfer_set):
                        dot.edge(str(i), str(j), color='red')
                    else:
                        dot.edge(str(i), str(j))
            elif i in errors_source_sink_set:
                dot.node(i, i + str(self.graph_record[i]), color='red')

        logging.info('start write visualization file...')
        dot.render(directory=output).replace('\\', '/')



