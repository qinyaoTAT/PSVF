import os
import source


def sink_arg():
    arg = source.source_arg()
    eval(arg)


def sink_env():
    env = source.source_env()
    os.system(env)


def sink_all():
    a, b, c = source.source_all()
    eval(a)
    eval(b)
    os.system(c)
    print(source.no_source())
