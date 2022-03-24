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
        var_name = inst_store.argval
        self.digraph.add_vertex(var_name)
        inst_rhs = self.utils.stack_pop()
        if inst_rhs.opname == 'LOAD_CONST':
            pass
        elif inst_rhs.opname == 'IMPORT_NAME' or inst_rhs.opname == 'IMPORT_FROM':
            pass
        elif inst_rhs.opname == 'BUILD_LIST':
            value_count = inst_rhs.argval
            for i in range(value_count):
                inst_list_value = self.utils.stack_pop()
                vertex_out = self.process_inst(inst_list_value)
                self.digraph.add_edge(vertex_out, var_name)


    def process_inst(self, inst):
        if inst.opname == 'LOAD_CONST':
            pass
        elif inst.opname == 'CALL_':
            pass
        return ''


