# -*- coding:utf-8 -*-
from src.utils import Utils
from src.digraph import Digraph
from src.builtin import BUILD_IN_FUNC_AND_ERROR

class Process:
    def __init__(self):
        self.utils = Utils()
        self.digraph = Digraph()

    def process_insts(self, insts):
        """
        功能描述： 处理python bytecode指令列表
        参数：
        返回值：
        异常描述：
        """
        for index, inst in enumerate(insts):
            try:
                # print(index)
                if inst.starts_line == 186:
                    print()
                self.utils.push(inst)

                self.process_store(inst)
                self.process_call(inst)
                self.process_build(inst)
                self.process_return(inst)

            except Exception as exception:
                pass

    def process_store(self, inst):
        self.process_store_name(inst)
        self.process_store_fast(inst)
        self.process_store_global(inst)
        self.process_store_deref(inst)
        self.process_store_subscr(inst)
        self.process_store_attr(inst)

    def process_store_name(self, inst):
        if 'STORE_NAME' != inst.opname:
            return
        inst_store = self.utils.pop()
        value_lhs = inst_store.argval
        value_rhs = self.process_rhs()
        if value_rhs == 'MAKE_FUNCTION':
            self.digraph.add_vertex(value_lhs + '::-1')
        elif isinstance(value_rhs, str):
            self.digraph.add_edge(value_rhs, value_lhs)
        elif isinstance(value_rhs, set):
            for i in value_rhs:
                self.digraph.add_edge(i, value_lhs)


    def process_store_fast(self, inst):
        if 'STORE_FAST' != inst.opname:
            return
        inst_store = self.utils.pop()
        value_lhs = inst_store.argval
        self.digraph.add_vertex(value_lhs)
        value_rhs = self.process_rhs()
        if isinstance(value_rhs, str):
            self.digraph.add_edge(value_rhs, value_lhs)
        elif isinstance(value_rhs, set):
            for i in value_rhs:
                self.digraph.add_edge(i, value_lhs)

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

    def process_binary(self, inst):
        if 'BINARY_' not in inst.opname:
            return

    def process_build(self, inst):
        if 'BUILD_' not in inst.opname:
            return
        elem_count = inst.argval
        elem_set = set()
        build_inst = self.utils.pop()
        for i in range(elem_count):
            value_rhs = self.process_rhs()
            if isinstance(value_rhs, set):
                elem_set += value_rhs
            elif value_rhs:
                elem_set.add(value_rhs)
        self.utils.current_build_set = elem_set
        self.utils.push(build_inst)

    def process_call(self, inst):
        """
        功能描述： 处理函数调用
        参数：
        返回值：
        异常描述：
        """
        if 'CALL_' not in inst.opname:
            return
        call_inst = self.utils.pop()
        if 'CALL_' in inst.opname:
            args_count = inst.argval
            # key value参数去掉第一句key的LOAD_CONST
            if 'CALL_FUNCTION_KW' in inst.opname:
                self.utils.pop()
            args_list = self.process_args(args_count)

            func_name = ''
            if 'CALL_FUNCTION' in inst.opname:
                inst_func_name = self.utils.pop()
                if inst_func_name.opname == 'LOAD_GLOBAL':
                    func_name = inst_func_name.argval
                elif inst_func_name.opname == 'LOAD_ATTR':
                    attr_name = inst_func_name.argval
                    inst_global = self.utils.pop()
                    if inst_global.opname == 'LOAD_GLOBAL':
                        func_name = inst_global.argval + '.' + attr_name
                    elif inst_global.opname == 'LOAD_CONST':
                        func_name = attr_name

            elif 'CALL_METHOD' in inst.opname:
                inst_method_name = self.utils.pop()
                inst_global = self.utils.pop()
                if inst_method_name.argval in ['read', 'write']:
                    func_name = inst_method_name.argval
                elif inst_global.opname == 'LOAD_GLOBAL':
                    func_name = inst_global.argval + '.' + inst_method_name.argval
                elif inst_global.opname == 'LOAD_CONST':
                    func_name = inst_method_name.argval
                elif 'CALL_' in inst_global.opname:
                    func_name = self.utils.last_call_name + '.' + inst_method_name.argval
                elif inst_global.opname == 'LOAD_ATTR':
                    attr_name = inst_global.argval + '.' + inst_method_name.argval
                    inst_global = self.utils.pop()
                    if inst_global.opname == 'LOAD_GLOBAL':
                        func_name = inst_global.argval + '.' + attr_name
                    elif inst_global.opname == 'LOAD_CONST':
                        func_name = attr_name
                else:
                    func_name = inst_method_name.argval

            if not func_name:
                return

            # arg to func
            for index, inst in enumerate(args_list):
                if 'LOAD_FAST' == inst.opname or 'LOAD_NAME' == inst.opname:
                    vertex_in = func_name + '::' + str(index)
                    vertex_out = inst.argval
                    self.digraph.add_edge(vertex_out, vertex_in)
                elif 'LOAD_ATTR' == inst.opname:
                    vertex_out = args_list[index - 1].argval + '.' + inst.argval
                    vertex_in = func_name + '::' + str(index - 1)
                    self.digraph.add_edge(vertex_out, vertex_in)
                elif 'CALL_' in inst.opname:
                    vertex_in = func_name + '::' + str(index)
                    if self.utils.last_call_name:
                        vertex_out = self.utils.last_call_name + '::-1'
                        self.digraph.add_edge(vertex_out, vertex_in)
                elif 'BUILD_' in inst.opname:
                    vertex_in = func_name + '::' + str(index)
                    elem_set = self.utils.current_build_set
                    for vertex_out in elem_set:
                        self.digraph.add_edge(vertex_out, vertex_in)

            self.utils.last_call_name = func_name
            self.utils.push(call_inst)

    def process_return(self, inst):
        """
        功能描述： 处理函数返回值
        参数：
        返回值：
        异常描述：
        """
        if 'RETURN_VALUE' != inst.opname:
            return
        ret_inst = self.utils.pop()
        value_rhs = self.process_rhs()
        value_lhs = self.utils.current_func_name + '::-1'
        if isinstance(value_rhs, str):
            self.digraph.add_edge(value_rhs, value_lhs)
        elif isinstance(value_rhs, set):
            for i in value_rhs:
                self.digraph.add_edge(i, value_lhs)

    def process_args(self, args_count):
        args_list = []
        for i in range(args_count):
            inst = self.utils.pop()
            if 'LOAD_' in inst.opname:
                args_list.append(inst)
                if 'LOAD_ATTR' == inst.opname:
                    args_list.append(self.utils.pop())
            elif 'CALL_' in inst.opname:
                args_list.append(inst)
            elif 'BUILD_' in inst.opname:
                args_list.append(inst)
        args_list.reverse()

        return args_list

    def process_declaration_args(self, args_list):
        for index, value in enumerate(args_list):
            self.digraph.add_edge(self.utils.current_func_name + '::' + str(index), value)


    def process_rhs(self):
        inst_rhs = self.utils.pop()
        value_rhs = ''
        if 'LOAD_CONST' in inst_rhs.opname:
            pass
        elif 'LOAD_NAME' in inst_rhs.opname:
            value_rhs = inst_rhs.argval
        elif 'LOAD_FAST' in inst_rhs.opname:
            value_rhs = inst_rhs.argval
        elif inst_rhs.opname == 'IMPORT_NAME' or inst_rhs.opname == 'IMPORT_FROM':
            pass
        elif inst_rhs.opname == 'BUILD_LIST':
            return self.utils.current_build_set
        elif inst_rhs.opname == 'BUILD_DICT':
            pass
        elif 'CALL_FUNCTION' in inst_rhs.opname:
            value_rhs = self.utils.last_call_name + '::-1'
        elif inst_rhs.opname == 'MAKE_FUNCTION':
            value_rhs = 'MAKE_FUNCTION'
        elif inst_rhs.opname == 'COMPARE_OP':
            pass

        return value_rhs



