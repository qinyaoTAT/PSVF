import dis
import os
import sys
import re
import codecs
import logging
import platform

from src import process
from src import pre_process

logging.basicConfig(format="%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s", level=logging.INFO)
VERSION = '1.0.0'


class PSVF:
    def __init__(self):
        self.process = process.Process()

    def get_top_insts(self, file):
        top_level_insts = []
        with codecs.open(file, 'r', encoding='UTF-8', errors='strict') as fp:
            src_code = fp.read()
            # dis.dis(src_code)
            code_obj = dis.Bytecode(src_code)
            for inst in code_obj:
                top_level_insts.append(inst)
            co_consts = code_obj.codeobj.co_consts
        self.process.process_insts(top_level_insts)
        self.process.utils.clean()
        self.get_sub_body_insts(co_consts, type(code_obj.codeobj))

    def get_sub_body_insts(self, co_consts, codeobj_type):
        for sub_codeobj in co_consts:
            if isinstance(sub_codeobj, codeobj_type):
                body_insts = []
                body_co_consts = sub_codeobj.co_consts
                func_or_class_name = sub_codeobj.co_name
                co_varnames = sub_codeobj.co_varnames
                co_argcount = sub_codeobj.co_argcount
                self.process.utils.current_func_name = func_or_class_name
                if co_argcount > 0:
                    args_list = co_varnames[:co_argcount]
                    self.process.process_declaration_args(args_list)
                sub_body_insts = dis.get_instructions(sub_codeobj)
                for inst in sub_body_insts:
                    body_insts.append(inst)

                self.process.process_insts(body_insts)
                if body_co_consts:
                    self.get_sub_body_insts(body_co_consts, codeobj_type)

    def run(self):
        args = pre_process.arg_parser()
        output = args.output
        scan_path = args.scan_path
        if not os.path.exists(scan_path):
            logging.error('please specify the correct scan path!!!')
            exit(-1)
        if not os.path.exists(output):
            logging.error('please specify the correct output directory!!!')
            exit(-1)

        file_list, module_set = pre_process.get_file_list(scan_path)
        for file in file_list:
            module_name = file.replace(scan_path, '')[1:-3]
            module_name = module_name.replace(os.sep, '.')
            self.get_top_insts(file)
            self.process.digraph.write(module_name=module_name)

            break


if __name__ == '__main__':
    psvf = PSVF()
    psvf.run()



