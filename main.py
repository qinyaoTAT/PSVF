import dis
import os
import sys
import re
import symtable
import logging
import graphviz

from argparse import ArgumentParser

logging.basicConfig(format="%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s", level=logging.INFO)
source_path = 'D:\deeplearninglib_top10\\tensorflow-master'
VERSION = '1.0.0'


class PSVF:
    def __init__(self, path):
        self.path = path

    def arg_parser(self):
        arg = ArgumentParser(description="PSVF")
        arg.add_argument("-o", '--output', dest='output', help="specify the output directory.", default='.')
        arg.add_argument("-v", '--version', help="show version.")
        return arg.parse_args()

    def get_file_list(self):
        file_list = []
        module_set = set()
        for root, dirs, files in os.walk(self.path, topdown=True):
            for name in files:
                if name.endswith('.py'):
                    abs_path = os.path.join(root, name)
                    file_list.append(abs_path)
                    module_name = abs_path.replace(source_path, '')
                    module_name = module_name.replace('.py', '')
                    module_name = module_name.replace(os.sep, '.')
                    if module_name.startswith('.'):
                        module_name = module_name[1:]
                    if module_name.endswith('.__init__'):
                        module_name = module_name.replace('.__init__', '')
                    module_set.add(module_name)
        return file_list, module_set

    def run(self):
        args = self.arg_parser()
        output = args.output
        if not os.path.exists(output):
            logging.error('please specify the correct output directory!!!')
            exit(-1)
        if os.path.isdir(output):
            output = os.path.join(output, 'out.png')

        dot = graphviz.Digraph('PSVF', comment='the psvf')
        dot.node('a', 'a')
        dot.node('b', 'b')
        dot.node('c', 'c')
        dot.edges(['ab', 'ac'])
        dot.edge('b', 'c', constrait='false')
        dot.format = 'png'
        print(dot.source)
        dot.render(directory='output').replace('\\', '/')

        file_list, module_set = self.get_file_list()
        for file in file_list:
            f = open(file, 'r')
            # dis.dis(f.read())
            code_obj = dis.get_instructions(f.read())
            for i in code_obj:
                if 'STORE_' in i.opname:
                    pass


if __name__ == '__main__':
    psvf = PSVF(source_path)
    psvf.run()



