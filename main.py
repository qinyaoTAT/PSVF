import dis
import os
import sys
import re
import codecs
import logging
import graphviz



from src import process
from src import pre_process

logging.basicConfig(format="%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s", level=logging.INFO)
source_path = 'D:\deeplearninglib_top10\\tensorflow-master'
VERSION = '1.0.0'


class PSVF:
    def __init__(self, path):
        self.path = path
        file_list, module_set = pre_process.get_file_list(self.path)
        self.file_list = file_list
        self.module_set = module_set
        self.process = process.Process()

    def get_top_insts(self, file):
        top_level_insts = []
        with codecs.open(file, 'r', encoding='UTF-8', errors='strict') as fp:
            src_code = fp.read()
            code_obj = dis.Bytecode(src_code)
            # dis.dis(f.read())
            for inst in code_obj:
                top_level_insts.append(inst)
            co_consts = code_obj.codeobj.co_consts
        self.process.process_insts(top_level_insts)
        self.get_sub_body_insts(co_consts, type(code_obj.codeobj))

    def get_sub_body_insts(self, co_consts, codeobj_type):
        for sub_codeobj in co_consts:
            if isinstance(sub_codeobj, codeobj_type):
                body_insts = []
                body_co_consts = sub_codeobj.co_consts
                sub_body_insts = dis.get_instructions(sub_codeobj)
                for inst in sub_body_insts:
                    body_insts.append(inst)

                self.process.process_insts(body_insts)
                if body_co_consts:
                    self.get_sub_body_insts(body_co_consts, codeobj_type)

    def run(self):
        args = pre_process.arg_parser()
        output = args.output
        if not os.path.exists(output):
            logging.error('please specify the correct output directory!!!')
            exit(-1)
        if os.path.isdir(output):
            output = os.path.join(output, 'out.png')

        for file in self.file_list:
            module_name = file.replace(self.path, '')[1:-3]
            module_name = module_name.replace(os.sep, '.')
            self.get_top_insts(file)


if __name__ == '__main__':
    psvf = PSVF(source_path)
    psvf.run()



