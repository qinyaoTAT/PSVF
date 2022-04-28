# -*- coding:utf-8 -*-
import json
import logging
import queue
import os
import copy

from src import rules

class DFS:
    def __init__(self, graph):
        self.graph = graph
        self.start_vertex = set()
        self.trace = []
        self.errors = []
        self.get_start_vertex()
        self.load_rules = rules.Rules(os.path.join('rules', 'rules.json'))
        self.load_rules.get_rules()

    def get_start_vertex(self):
        # 获取所有起始顶点
        self.start_vertex = set(self.graph.keys())
        sub_vertext_set = set()
        for vertex in self.graph:
            sub_vertext_set |= set(self.graph[vertex])
        for i in sub_vertext_set:
            if i in self.start_vertex:
                self.start_vertex.remove(i)

    def analyze(self):
        for vertex in self.start_vertex:
            visited_vertex = set()
            visited_vertex.add(vertex)
            self.dfs(vertex, visited_vertex)

    def dfs(self, vertex, visited_vertex):
        # source
        source_vertex = False
        if self.is_source(vertex):
            self.trace.append(vertex)
            source_vertex = True
        # clean
        if self.is_clean(vertex):
            return
        # sink
        if self.trace and self.is_sink(vertex):
            self.trace.append(vertex)
            # find one path(source -> sink)
            tmp = copy.deepcopy(self.trace)
            if tmp not in self.errors:
                self.errors.append(tmp)
            self.trace.pop()
            return

        # transfer path
        if self.trace and not source_vertex:
            self.trace.append(vertex)

        for i in self.graph[vertex]:
            if i not in visited_vertex:
                visited_vertex.add(i)
                self.dfs(i, visited_vertex)

        if self.trace:
            self.trace.pop()

    def is_source(self, vertex):
        source_dict = self.load_rules.source
        for rule_name in source_dict:
            if 'function' in source_dict[rule_name]:
                functions = source_dict[rule_name]['function']
                for i in functions:
                    if i == vertex:
                        return True
        return False

    def is_sink(self, vertex):
        sink_dict = self.load_rules.sink
        for rule_name in sink_dict:
            if 'function' in sink_dict[rule_name]:
                functions = sink_dict[rule_name]['function']
                for i in functions:
                    if i == vertex:
                        return True
        return False

    def is_clean(self, vertex):
        clean_dict = self.load_rules.clean
        for rule_name in clean_dict:
            if 'function' in clean_dict[rule_name]:
                functions = clean_dict[rule_name]['function']
                for i in functions:
                    if i in vertex:
                        return True
        return False

    def report(self, output, fmt):
        if self.errors:
            out_data = {
                'errors': []
            }
            for error in self.errors:
                logging.warning('Found source(' + str(error[0]) + ') to sink(' + str(error[-1]) + ')')
                error_detail = {}
                error_detail['transfer'] = []
                for index, data in enumerate(error):
                    if index == 0:
                        error_detail['source'] = {
                            'value': data,
                            'lineno': ''
                        }
                    elif index == len(error) - 1:
                        error_detail['sink'] = {
                            'value': data,
                            'lineno': ''
                        }
                    else:
                        error_detail['transfer'].append({
                            'value': data,
                            'lineno': ''
                        })
                out_data['errors'].append(error_detail)
            logging.warning('Found ' + str(len(self.errors)) + ' Errors!!!')
            if fmt == 'json':
                with open(output, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(out_data, indent=2, ensure_ascii=False, sort_keys=True))
                    logging.info('Write Report File: ' + output)
                with open(output[:-4] + '_origin.json', 'w', encoding='utf-8') as f:
                    f.write(json.dumps(self.graph, indent=2, ensure_ascii=False, sort_keys=True))
        else:
            logging.warning('Not Found Errors!!!')
