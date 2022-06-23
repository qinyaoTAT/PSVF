# -*- coding:utf-8 -*-

class Utils:
    def __init__(self):
        '''
        record information
        '''
        self.insts_stack = []
        self.project_module_set = set()
        self.current_function_set = set()
        self.current_func_name = ''
        self.current_module_name = ''
        self.called_name = []
        self.rot_value = []
        self.current_lineno = 0
        self.build_elem_set = set()
        self.binary_operand_set = set()
        self.current_whole_name = dict()

    def push(self, inst):
        '''
        stack push
        :param inst:
        :return:
        '''
        self.insts_stack.append(inst)

    def pop(self):
        '''
        stack pop
        :return:
        '''
        if self.insts_stack:
            inst = self.insts_stack.pop()
            return inst
        else:
            return None

    def clean(self):
        self.insts_stack = []