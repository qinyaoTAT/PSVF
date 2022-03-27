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
                self.utils.push(inst)

                self.process_store_name(inst)
                self.process_store_fast(inst)
                self.process_store_global(inst)
                self.process_store_deref(inst)
                self.process_store_subscr(inst)
                self.process_store_attr(inst)
            except Exception as exception:
                pass

    def process_store_name(self, inst):
        if 'STORE_NAME' != inst.opname:
            return
        inst_store = self.utils.pop()
        value_lhs = inst_store.argval
        self.digraph.add_vertex(value_lhs)
        self.process_rhs(value_lhs)

    def process_store_fast(self, inst):
        if 'STORE_FAST' != inst.opname:
            return
        inst_store = self.utils.pop()
        value_lhs = inst_store.argval
        self.digraph.add_vertex(value_lhs)
        self.process_rhs(value_lhs)

    def process_store_global(self, inst):
        pass

    def process_store_deref(self, inst):
        pass

    def process_store_subscr(self, inst):
        pass

    def process_store_attr(self, inst):
        pass

    def process_import(self, inst):
        pass

    def process_build_list(self, inst):
        pass

    def process_call(self, inst):
        if 'CALL_' not in inst.opname:
            return
        args_count = inst.argval
        inst_args = []
        for i in range(args_count):
            inst_args.append(self.utils.pop())
        inst_args.reverse()
        # arg to func

        self.utils.push(inst)


        # func to value
        # inst_func_name = self.utils.pop()
        # if inst_func_name.opname == 'LOAD_GLOBAL':
        #     func_name = inst_func_name.argval
        #     func_name = func_name + '::-1'
        #     self.digraph.add_edge(func_name, value_lhs)


    def process_rhs(self, value_lhs):
        inst_rhs = self.utils.pop()
        if 'LOAD_' in inst_rhs.opname:
            pass
        elif inst_rhs.opname == 'IMPORT_NAME' or inst_rhs.opname == 'IMPORT_FROM':
            pass
        elif inst_rhs.opname == 'BUILD_LIST':
            value_count = inst_rhs.argval
            for i in range(value_count):
                inst_list_value = self.utils.pop()
                vertex_out = self.process_rhs(inst_list_value)
                self.digraph.add_edge(vertex_out, value_lhs)
        elif inst_rhs.opname == 'BUILD_DICT':
            pass
        elif 'CALL_' in inst_rhs.opname:
            self.process_call(inst_rhs, value_lhs)

        elif inst_rhs.opname == 'MAKE_FUNCTION':
            self.digraph.del_vertex(value_lhs)
            self.digraph.add_vertex(value_lhs + '::-1')



