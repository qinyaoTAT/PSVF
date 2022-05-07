# -*- coding:utf-8 -*-
import os

import graphviz
import logging


class Digraph:
    def __init__(self):
        # graph 的节点值不要手动修改
        self.graph = {}
        # 记录位置信息
        self.graph_record = {}
        self.lineno = 0
        self.file_path = ''

    def add_vertex(self, value):
        if not value or not isinstance(value, str):
            return
        if value not in self.graph:
            self.graph[value] = []
            self.graph_record[value] = {
                'lineno': set(),
                'path': set()
            }
        self.graph_record[value]['lineno'].add(self.lineno)
        self.graph_record[value]['path'].add(self.file_path)

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
        self.add_vertex(vertex_in)
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
                    if i in errors_source_sink_set:
                        dot.node(i, color='red')
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

        logging.info('start write project visualization file...')
        dot.render(directory=output).replace('\\', '/')

    def generate_errors(self, output, errors, project_name):
        dot = graphviz.Digraph(project_name + '_errors', comment='generate source --> sink graph.', strict=True,
                               node_attr={'color': 'lightblue2', 'style': 'filled', 'shape': 'box'})
        dot.format = 'png'
        for i in errors:
            for j in i:
                detail = j + os.linesep + 'path:' + str(self.graph_record[j]['path']) + os.linesep + 'lineno:' + str(self.graph_record[j]['lineno'])
                if j == i[0] or j == i[-1]:
                    dot.node(j, detail, color='red')
                else:
                    dot.node(j, detail)
            for j in range(len(i) - 1):
                dot.edge(i[j], i[j + 1])

        logging.info('start write errors visualization file...')
        dot.render(directory=output).replace('\\', '/')
