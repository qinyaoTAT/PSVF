# -*- coding:utf-8 -*-
import json
import os
import logging
import time
import datetime

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
        is_graph = args.graph
        is_output_format = args.format
        if not os.path.exists(scan_path):
            logging.error('please specify the correct scan path!!!')
            exit(-1)
        if not os.path.exists(output):
            logging.error('please specify the correct output directory!!!')
            exit(-1)

        project_name = scan_path.split(os.sep)[-1]
        file_list, project_module_set = pre_process.get_file_list(scan_path)
        self.process.utils.project_module_set = project_module_set


        start_time = int(time.time())
        counter = 0
        for file in file_list:
            logging.info('process file: ' + file)
            module_name = file.replace(scan_path, '')[1:-3]
            module_name = module_name.replace(os.sep, '.')
            function_name_set = pre_process.get_function_name(file)
            self.process.utils.current_function_set = function_name_set
            self.process.utils.current_module_name = module_name
            self.process.process_top_insts(file)

            counter += 1
            if counter > 100:
                break
            # self.process.process_top_insts('')
            # break

        logging.info('start analyze graph...')
        analyze = analyzer.DFS(self.process.digraph.graph)
        analyze.analyze()
        if os.path.isdir(output):
            output_report = os.path.join(output, project_name + '.json')
            logging.info('start generate report...')
            analyze.report(output_report, is_output_format)

        if is_graph:
            logging.info('start generate pdf graph...')
            self.process.digraph.generate(output, analyze.errors, project_name=project_name)

        end_time = int(time.time())
        use_time = end_time - start_time
        data_array = datetime.datetime.utcfromtimestamp(use_time)
        logging.info('Total Time: ' + str(data_array.strftime('%H:%M:%S')))
        logging.info('Total Lines: ' + str(pre_process.ALL_LINES))


if __name__ == '__main__':
    psvf = PSVF()
    psvf.run()



