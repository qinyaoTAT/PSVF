![psvf.png](doc/psvf.png) 

Python Static Value-Flow Analysis Framework

## Overview

PSVF is a tool designed to find common security issues in Python code. Based on python bytecode, builds Value-Flow graph, and analyze graph.

example:

![img.png](doc/example_graph.png)

## Usage

```buildoutcfg
usage: psvf.py [-h] [-s SCAN_PATH] [-o OUTPUT] [-f FMT] [-v VERSION]

Python Static Value-Flow Analysis Framework

optional arguments:
  -h, --help            show this help message and exit
  -s SCAN_PATH, --scan_path SCAN_PATH
                        specify the scan directory.
  -o OUTPUT, --output OUTPUT
                        specify the output directory.
  -f FMT, --fmt FMT     generate graph file's format.
  -v VERSION, --version VERSION
                        show version.


```

## TODO
 - 装饰器值流图构建
 - 类继承值流图构建
 - 跨文件值流图构建