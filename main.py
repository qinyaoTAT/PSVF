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


def arg_parser():
    argParser = ArgumentParser(description="PSVF")
    argParser.add_argument("-o", '--output', dest='output', help="specify the output directory.", default='.')
    return argParser.parse_args()


def get_file_list():
    file_list = []
    for root, dirs, files in os.walk(source_path, topdown=True):
        for name in files:
            if name.endswith('.py'):
                abs_path = os.path.join(root, name)
                file_list.append(abs_path)
    return file_list


def main():
    args = arg_parser()
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



    f = open('test/configure.py', 'r')
    # dis.dis(f.read())
    code_obj = dis.get_instructions(f.read())
    for i in code_obj:
        if i.opname == 'STORE_FAST':
            pass


    print()




if __name__ == '__main__':
    main()


