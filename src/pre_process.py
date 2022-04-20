# -*- coding:utf-8 -*-
import os

from argparse import ArgumentParser

IS_COUNT_LINE = 1
ALL_LINES = 0


def arg_parser():
    arg = ArgumentParser(description="Python Static Value-Flow Analysis Framework")
    arg.add_argument("-s", '--scan_path', dest='scan_path', help="specify the scan directory.", default='')
    arg.add_argument("-o", '--output', dest='output', help="specify the output directory.", default='output')
    arg.add_argument("-g", '--graph', action='store_true', help="generate graph file.")
    arg.add_argument("-v", '--version', help="show version.")
    return arg.parse_args()


def get_file_list(path):
    file_list = []
    module_set = set()
    if os.path.isfile(path):
        path = os.path.realpath(path)
        file_list.append(path)
        module_name = os.path.basename(path)
        module_name = module_name.replace('.py', '')
        module_set.add(module_name)
        return file_list, module_set
    for root, dirs, files in os.walk(path, topdown=True):
        for name in files:
            if name.endswith('.py'):
                abs_path = os.path.join(root, name)
                get_lines(abs_path)
                file_list.append(abs_path)
                module_name = abs_path.replace(path, '')
                module_name = module_name.replace('.py', '')
                module_name = module_name.replace(os.sep, '.')
                if module_name.startswith('.'):
                    module_name = module_name[1:]
                if module_name.endswith('.__init__'):
                    module_name = module_name.replace('.__init__', '')
                module_set.add(module_name)
    return file_list, module_set


def get_lines(file):
    if IS_COUNT_LINE:
        with open(file, 'r', encoding='utf-8') as f:
            global ALL_LINES
            while True:
                buffer = f.read(1024 * 1024)
                if not buffer:
                    break
                ALL_LINES += buffer.count('\n')
