# -*- coding:utf-8 -*-
from src.utils import Utils
from src.digraph import Digraph

class Process:
    def __init__(self):
        self.utils = Utils()
        self.digraph = Digraph()

    def process_insts(self, insts):
        for index, inst in enumerate(insts):
            try:
                # print(index)
                self.utils.stack_push(inst)

                self.process_store_name(inst)
            except Exception as exception:
                pass

    def process_store_name(self, inst):
        if 'STORE_NAME' != inst.opname:
            return
        inst_store = self.utils.stack_pop()
        value_lhs = inst_store.argval
        self.digraph.add_vertex(value_lhs)
        inst_rhs = self.utils.stack_pop()
        self.process_value_rhs(inst_rhs, value_lhs)
        

    def process_value_rhs(self, inst_rhs, value_lhs):
        if 'LOAD_' in inst_rhs.opname:
            pass
        elif inst_rhs.opname == 'IMPORT_NAME' or inst_rhs.opname == 'IMPORT_FROM':
            pass
        elif inst_rhs.opname == 'BUILD_LIST':
            value_count = inst_rhs.argval
            for i in range(value_count):
                inst_list_value = self.utils.stack_pop()
                vertex_out = self.process_value_rhs(inst_list_value)
                self.digraph.add_edge(vertex_out, value_lhs)
        elif inst_rhs.opname == 'BUILD_DICT':
            pass
        elif inst_rhs.opname == 'CALL_FUNCTION':
            pass
        elif inst_rhs.opname == 'MAKE_FUNCTION':
            pass


