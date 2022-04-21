import sys
import os


def source_arg():
    ret = sys.argv
    return ret[0]

def source_env():
    ret = os.environ
    return ret

def source_all():
    a, b, c = source_arg(), source_env(), os.environ
    return a, b, c
