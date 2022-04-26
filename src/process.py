# -*- coding:utf-8 -*-
import logging
import dis
import codecs

from src.utils import Utils
from src.digraph import Digraph
from src.common import BUILD_IN_FUNC, BUILD_IN_STR_METHOD, BUILD_IN_DICT_METHOD, BUILD_IN_PASS_METHOD, BUILD_IN_MODEL_FUNC

class Process:
    def __init__(self):
        self.utils = Utils()
        self.digraph = Digraph()

    def get_whole_name(self, name):
        if self.utils.current_module_name:
            return self.utils.current_module_name + '.' + name
        return name

    def process_top_insts(self, file):
        top_level_insts = []
        with codecs.open(file, 'r', encoding='UTF-8', errors='strict') as fp:
            src_code = fp.read()
            # dis.dis(src_code)
            code_obj = dis.Bytecode(src_code)
            for inst in code_obj:
                top_level_insts.append(inst)
            co_consts = code_obj.codeobj.co_consts
        self.utils.current_import_module = dict()
        self.process_insts(top_level_insts)
        self.utils.clean()
        self.process_sub_body_insts(co_consts, type(code_obj.codeobj))

    def process_sub_body_insts(self, co_consts, codeobj_type):
        for sub_codeobj in co_consts:
            if isinstance(sub_codeobj, codeobj_type):
                body_insts = []
                body_co_consts = sub_codeobj.co_consts
                func_or_class_name = sub_codeobj.co_name
                co_varnames = sub_codeobj.co_varnames
                co_argcount = sub_codeobj.co_argcount
                self.utils.current_func_name = self.get_whole_name(func_or_class_name)
                if co_argcount > 0:
                    args_list = co_varnames[:co_argcount]
                    self.process_declaration_args(args_list)
                sub_body_insts = dis.get_instructions(sub_codeobj)
                for inst in sub_body_insts:
                    body_insts.append(inst)

                self.process_insts(body_insts)
                if body_co_consts:
                    self.process_sub_body_insts(body_co_consts, codeobj_type)

    def process_insts(self, insts):
        """
        """
        for index, inst in enumerate(insts):
            try:
                if inst.starts_line:
                    self.utils.current_lineno = inst.starts_line
                    self.digraph.lineno = inst.starts_line
                    if inst.starts_line == 1303:
                        print()

                self.utils.push(inst)

                self.process_rot(inst)
                self.process_unpack(inst)
                self.process_store(inst)
                self.process_call(inst)
                self.process_build(inst)
                self.process_return(inst)
                self.process_binary(inst)
                self.process_compare_op(inst)

            except Exception as exception:
                logging.warning(inst.opname + ' : ' + str(self.utils.current_lineno) + ':' + str(exception))

    def process_rot(self, inst):
        if 'ROT_' not in inst.opname:
            return
        rot_inst = self.utils.pop()
        count = 0
        if inst.opname == 'ROT_TWO':
            count = 2
            last_inst = self.utils.pop()
            if last_inst.opname == 'ROT_THREE':
                self.utils.push(last_inst)
                return
        elif inst.opname == 'ROT_THREE':
            count = 3
        for i in range(count):
            value_rhs = self.process_rhs()
            self.utils.rot_value.append(value_rhs)
        self.utils.push(rot_inst)

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
        value_lhs = self.get_whole_name(value_lhs)
        value_rhs = self.process_rhs(value_lhs=value_lhs)
        if not value_rhs:
            return
        elif value_rhs == 'MAKE_FUNCTION':
            self.digraph.add_vertex(value_lhs + '#-1')
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
        if self.utils.current_func_name:
            value_lhs = self.utils.current_func_name + '.' + value_lhs
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
        if 'STORE_SUBSCR' not in inst.opname:
            return
        inst_store = self.utils.pop()
        index_inst = self.utils.pop()
        value_lhs_inst = self.utils.pop()
        value_lhs = value_lhs_inst.argval
        if self.utils.current_func_name:
            value_lhs = self.utils.current_func_name + '.' + value_lhs
        self.digraph.add_vertex(value_lhs)
        value_rhs = self.process_rhs()
        if isinstance(value_rhs, str):
            self.digraph.add_edge(value_rhs, value_lhs)
        elif isinstance(value_rhs, set):
            for i in value_rhs:
                self.digraph.add_edge(i, value_lhs)


    def process_store_attr(self, inst):
        pass

    def process_unpack(self, inst):
        '''
        :param inst: 当前指令
        :return: 无
        '''
        if 'UNPACK_SEQUENCE' != inst.opname:
            return
        unpack_inst = self.utils.pop()
        last_inst = self.utils.pop()
        if 'CALL_' in last_inst.opname:
            last_call_name = self.utils.called_name.pop()
            count = inst.argval
            for i in range(count):
                self.utils.push(last_inst)
                self.utils.called_name.append(last_call_name)

    def process_import(self, inst, value_lhs):
        if 'IMPORT_' not in inst.opname:
            return
        import_name = ''
        if 'IMPORT_NAME' == inst.opname:
            import_name = inst.argval
        elif 'IMPORT_FROM' == inst.opname:
            import_name = inst.argval
            inst_name = self.utils.pop()
            if 'IMPORT_NAME' == inst_name.opname:
                import_name = inst_name.argval + '.' + import_name
        self.utils.current_import_module[value_lhs] = import_name

    def process_binary(self, inst):
        if 'BINARY_' not in inst.opname:
            return
        binary_inst = self.utils.pop()
        if 'BINARY_SUBSCR' in inst.opname:
            index_inst = self.utils.pop()
            return
        elif 'BINARY_' in inst.opname:
            for i in range(2):
                value = self.process_rhs()
                if isinstance(value, str):
                    self.utils.current_operand_set.add(value)
                elif isinstance(value, set):
                    self.utils.current_operand_set |= value
            self.utils.push(binary_inst)

    def process_load_name(self, value):
        if value in self.utils.current_import_module:
            return self.utils.current_import_module[value]
        elif value in self.utils.project_module_set:
            return self.utils.current_module_name + '.' + value
        else:
            return value

    def process_build(self, inst):
        if 'BUILD_SLICE' in inst.opname:
            # 切片指令过滤
            inst_r = self.utils.pop()
            inst_l = self.utils.pop()
            return
        if 'BUILD_' not in inst.opname or 'LOAD_BUILD_CLASS' == inst.opname:
            return
        elem_count = inst.argval
        elem_set = set()
        build_inst = self.utils.pop()
        for i in range(elem_count):
            value_rhs = self.process_rhs()
            if isinstance(value_rhs, set):
                elem_set |= value_rhs
            elif value_rhs:
                elem_set.add(value_rhs)
        self.utils.current_build_set = elem_set
        self.utils.push(build_inst)

    def process_call(self, inst):
        """
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
                    func_name = self.utils.current_module_name + '.' + inst_func_name.argval
                elif inst_func_name.opname == 'LOAD_ATTR':
                    attr_name = inst_func_name.argval
                    inst_global = self.utils.pop()
                    if inst_global.opname == 'LOAD_GLOBAL':
                        func_name = inst_global.argval + '.' + attr_name
                    elif inst_global.opname == 'LOAD_CONST':
                        func_name = attr_name
                    elif inst_global.opname == 'LOAD_NAME':
                        value_name = self.process_load_name(inst_global.argval)
                        func_name = value_name + '.' + attr_name

            elif 'CALL_METHOD' in inst.opname:
                inst_method_name = self.utils.pop()
                inst_global = self.utils.pop()
                if inst_method_name.argval in BUILD_IN_STR_METHOD:
                    if inst_global.opname == 'LOAD_FAST' or inst_global.opname == 'LOAD_NAME':
                        self.utils.push(inst_global)
                    func_name = 'str.' + inst_method_name.argval
                    self.digraph.add_edge(func_name + '#0', func_name + '#-1')
                elif inst_method_name.argval in BUILD_IN_DICT_METHOD:
                    self.utils.push(inst_global)
                    return
                elif inst_method_name.argval in ['read', 'write']:
                    func_name = inst_method_name.argval
                elif inst_method_name.argval in BUILD_IN_PASS_METHOD:
                    if not args_list:
                        return
                    vertex_in = inst_global.argval
                    for arg in args_list:
                        if isinstance(arg, set):
                            for i in arg:
                                self.digraph.add_edge(i, vertex_in)
                        elif arg:
                            self.digraph.add_edge(arg, vertex_in)
                    return
                elif inst_global.opname == 'LOAD_GLOBAL':
                    func_name = inst_global.argval + '.' + inst_method_name.argval
                elif inst_global.opname == 'LOAD_CONST':
                    func_name = inst_method_name.argval
                elif inst_global.opname == 'LOAD_NAME':
                    value = self.process_load_name(inst_global.argval)
                    func_name = value + '.' + inst_method_name.argval
                elif 'CALL_' in inst_global.opname:
                    last_func_name = self.utils.called_name.pop()
                    func_name = last_func_name + '.' + inst_method_name.argval
                elif inst_global.opname == 'LOAD_ATTR':
                    attr_name = inst_global.argval + '.' + inst_method_name.argval
                    inst_global = self.utils.pop()
                    if inst_global.opname == 'LOAD_GLOBAL':
                        func_name = inst_global.argval + '.' + attr_name
                    elif inst_global.opname == 'LOAD_CONST':
                        func_name = attr_name
                    elif inst_global.opname == 'LOAD_NAME':
                        value = self.process_load_name(inst_global.argval)
                        func_name = value + '.' + attr_name
                else:
                    func_name = inst_method_name.argval

            if not func_name:
                return
            if func_name in BUILD_IN_FUNC or func_name in BUILD_IN_MODEL_FUNC:
                self.digraph.add_edge(func_name + '#0', func_name + '#-1')

            # arg to func
            for index, arg_value in enumerate(args_list):
                if isinstance(arg_value, set):
                    vertex_in = func_name + '#' + str(index)
                    for i in arg_value:
                        self.digraph.add_edge(i, vertex_in)
                elif arg_value:
                    vertex_in = func_name + '#' + str(index)
                    self.digraph.add_edge(arg_value, vertex_in)

            self.utils.called_name.append(func_name)
            self.utils.push(call_inst)

    def process_compare_op(self, inst):
        """
        """
        if 'COMPARE_OP' != inst.opname:
            return
        if 'in' != inst.argval:
            return
        compare_inst = self.utils.pop()
        value_rhs = self.process_rhs()
        value_lhs_inst = self.utils.pop()
        if value_lhs_inst.opname == 'LOAD_FAST':
            value_lhs = value_lhs_inst.argval
            if isinstance(value_rhs, str):
                self.digraph.add_edge(value_rhs, value_lhs)
            elif isinstance(value_rhs, set):
                for i in value_rhs:
                    self.digraph.add_edge(i, value_lhs)


    def process_return(self, inst):
        """
        """
        if 'RETURN_VALUE' != inst.opname:
            return
        ret_inst = self.utils.pop()
        value_rhs = self.process_rhs()
        value_lhs = self.utils.current_func_name + '#-1'
        if isinstance(value_rhs, str):
            self.digraph.add_edge(value_rhs, value_lhs)
        elif isinstance(value_rhs, set):
            for i in value_rhs:
                self.digraph.add_edge(i, value_lhs)

    def process_args(self, args_count):
        args_list = []
        for i in range(args_count):
            value = self.process_rhs()
            args_list.append(value)
        args_list.reverse()

        return args_list

    def process_declaration_args(self, args_list):
        for index, value in enumerate(args_list):
            value_arg = value
            if self.utils.current_func_name:
                value_arg = self.utils.current_func_name + '.' + value
            self.digraph.add_edge(self.utils.current_func_name + '#' + str(index), value_arg)

    def process_rhs(self, value_lhs=''):
        inst_rhs = self.utils.pop()
        value_rhs = ''
        if 'LOAD_CONST' in inst_rhs.opname:
            pass
        elif 'LOAD_NAME' in inst_rhs.opname:
            value_rhs = self.process_load_name(inst_rhs.argval)
        elif 'LOAD_FAST' in inst_rhs.opname:
            value_rhs = inst_rhs.argval
            if self.utils.current_func_name:
                value_rhs = self.utils.current_func_name + '.' + value_rhs
        elif 'LOAD_ATTR' in inst_rhs.opname:
            attr_value = inst_rhs.argval
            inst_global = self.utils.pop()
            while inst_global.opname == 'LOAD_ATTR':
                attr_value = inst_global.argval + '.' + attr_value
                inst_global = self.utils.pop()
            if 'LOAD_FAST' in inst_global.opname:
                value_rhs = inst_global.argval
            elif 'LOAD_GLOBAL' in inst_global.opname:
                value_rhs = inst_global.argval + '.' + attr_value
            elif 'LOAD_NAME' in inst_global.opname:
                value_rhs = self.process_load_name(inst_global.argval) + '.' + attr_value
            else:
                value_rhs = attr_value
        elif 'IMPORT_' in inst_rhs.opname:
            self.process_import(inst_rhs, value_lhs)
            return
        elif 'BUILD_' in inst_rhs.opname:
            if 'BUILD_SLICE' in inst_rhs.opname:
                return ''
            return self.utils.current_build_set
        elif 'CALL_' in inst_rhs.opname:
            func_name = self.utils.called_name.pop()
            if isinstance(func_name, str):
                value_rhs = func_name + '#-1'
        elif inst_rhs.opname == 'MAKE_FUNCTION':
            value_rhs = 'MAKE_FUNCTION'
        elif inst_rhs.opname == 'COMPARE_OP':
            pass
        elif 'BINARY_' in inst_rhs.opname:
            return self.utils.current_operand_set
        elif inst_rhs.opname == 'FOR_ITER':
            self.utils.pop()
            value_rhs = self.process_rhs()
        elif 'ROT_' in inst_rhs.opname:
            if self.utils.rot_value:
                value_rhs = self.utils.rot_value.pop()
            self.utils.push(inst_rhs)
        return value_rhs



