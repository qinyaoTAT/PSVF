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
        if not os.path.exists(scan_path):
            logging.error('please specify the correct scan path!!!')
            exit(-1)
        if not os.path.exists(output):
            logging.error('please specify the correct output directory!!!')
            exit(-1)

        project_name = scan_path.split(os.sep)[-1]
        file_list, module_set = pre_process.get_file_list(scan_path)

        start_time = int(time.time())
        for file in file_list:
            logging.info('process file: ' + file)
            module_name = file.replace(scan_path, '')[1:-3]
            module_name = module_name.replace(os.sep, '.')
            self.process.utils.current_module_name = module_name
            self.process.process_top_insts(file)
            # self.process.process_top_insts('D:\deeplearninglib_top10\\tensorflow-master\\tensorflow\compiler\mlir\\tfr\examples\mnist\mnist_train.py')
            # break
            # if 'api_template_v1.__init__.py' in file:
            #     break

        if is_graph:
            logging.info('start generate pdf graph...')
            self.process.digraph.generate(output, project_name=project_name)

        logging.info('start analyze graph...')
        analyze = analyzer.DFS(self.process.digraph.graph)
        analyze.analyze()
        if os.path.isdir(output):
            output = os.path.join(output, project_name + '.json')
        logging.info('start generate report...')
        analyze.report(output)

        with open('output/tensorflow_value_flow.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.process.digraph.graph, indent=2, ensure_ascii=False, sort_keys=True))

        end_time = int(time.time())
        use_time = end_time - start_time
        data_array = datetime.datetime.utcfromtimestamp(use_time)
        logging.info('Total Time: ' + str(data_array.strftime('%H:%M:%S')))
        logging.info('Total Lines: ' + str(pre_process.ALL_LINES))


if __name__ == '__main__':
    psvf = PSVF()
    psvf.run()



