# -*- coding:utf-8 -*-
import os
from argparse import ArgumentParser

def arg_parser():
    arg = ArgumentParser(description="PSVF")
    arg.add_argument("-o", '--output', dest='output', help="specify the output directory.", default='.')
    arg.add_argument("-v", '--version', help="show version.")
    return arg.parse_args()


def get_file_list(path):
    file_list = []
    module_set = set()
    for root, dirs, files in os.walk(path, topdown=True):
        for name in files:
            if name.endswith('.py'):
                abs_path = os.path.join(root, name)
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
