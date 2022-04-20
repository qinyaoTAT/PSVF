![psvf.png](doc/psvf.png) 

Python Static Value-Flow Analysis Framework

Advantage:
- Based on Value-Flow graph
- Supports data flow across files
- Pure python implementation
- Unbelievably fast (18w lines / 1 minute)

## Overview

PSVF is a tool designed to find vulnerability in Python code. Based on Value-Flow graph, and analyze it.

Example graph:

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