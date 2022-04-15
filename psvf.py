# -*- coding:utf-8 -*-
import os
import logging

from src import process
from src import pre_process
from src import analyzer

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)
VERSION = '1.0.0'


class PSVF:
    def __init__(self):
        self.process = process.Process()

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

        project_name = scan_path.split(os.sep)[-1]
        file_list, module_set = pre_process.get_file_list(scan_path)

        for file in file_list:
            module_name = file.replace(scan_path, '')[1:-3]
            module_name = module_name.replace(os.sep, '.')
            self.process.utils.current_module_name = module_name
            self.process.process_top_insts(file)
            break

        self.process.digraph.write(project_name=project_name)
        analyze = analyzer.DFS(self.process.digraph.graph)
        analyze.analyze()
        if os.path.isdir(output):
            output = os.path.join(output, project_name + '.json')
        analyze.report(output)


if __name__ == '__main__':
    psvf = PSVF()
    psvf.run()



