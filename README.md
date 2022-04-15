![psvf.png](doc/psvf.png) 

Python Static Value-Flow Analysis Framework

## Overview

PSVF is a tool designed to find common security issues in Python code. Based on python bytecode, builds Value-Flow graph, and analyze graph.



## Usage

```buildoutcfg
usage: psvf.py [-h] [-s SCAN_PATH] [-o OUTPUT] [-p PDF] [-v VERSION]

Python Static Value-Flow Analysis Framework

optional arguments:
  -h, --help            show this help message and exit
  -s SCAN_PATH, --scan_path SCAN_PATH
                        specify the scan directory.
  -o OUTPUT, --output OUTPUT
                        specify the output directory.
  -p PDF, --pdf PDF     generate PDF graph.
  -v VERSION, --version VERSION
                        show version.

```