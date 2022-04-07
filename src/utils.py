# -*- coding:utf-8 -*-

class Utils:
    def __init__(self):
        self.insts_stack = []
        self.current_func_name = ''
        self.last_call_name = ''
        self.current_lineno = 0
        self.current_build_set = set()
        self.current_operand_set = set()
        self.last_binary_subscr = ''

    def push(self, inst):
        self.insts_stack.append(inst)

    def pop(self):
        if self.insts_stack:
            inst = self.insts_stack.pop()
            return inst
        else:
            return None

    def clean(self):
        self.insts_stack = []