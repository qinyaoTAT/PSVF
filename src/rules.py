# -*- coding:utf-8 -*-
import json


class Rules:
    def __init__(self, path):
        self.path = path
        self.source = {}
        self.sink = {}
        self.transfer = {}
        self.clean = {}

    def get_rules(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            rules = json.loads(f.read())
            for i in rules:
                if i == 'source':
                    self.source = rules[i]
                elif i == 'sink':
                    self.sink = rules[i]
                elif i == 'transfer':
                    self.transfer = rules[i]
                elif i == 'clean':
                    self.clean = rules[i]


