# -*- coding:utf-8 -*-

class Process:
    def __init__(self):
        self.graph = {}

    def process_insts(self, insts):
        for index, inst in enumerate(insts):
            try:
                # print(index)
                self.process_inst(inst)
            except Exception as exception:
                pass

    def process_inst(self, inst):
        self.process_store_name(inst)

    def process_store_name(self, inst):
        if 'STORE_NAME' != inst.opname:
            return

