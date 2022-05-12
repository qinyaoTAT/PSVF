# -*- coding:utf-8 -*-

BUILD_IN_ERROR = ['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BlockingIOError',
                'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError',
                'ConnectionAbortedError', 'ConnectionError', 'ConnectionRefusedError',
                'ConnectionResetError', 'DeprecationWarning', 'EOFError', 'Ellipsis', 'EnvironmentError',
                'Exception', 'False', 'FileExistsError', 'FileNotFoundError', 'FloatingPointError',
                'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning',
                'IndentationError', 'IndexError', 'InterruptedError', 'IsADirectoryError', 'KeyError',
                'KeyboardInterrupt', 'LookupError', 'MemoryError', 'NameError', 'None',
                'NotADirectoryError', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError',
                'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError',
                'RecursionError', 'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning',
                'StopAsyncIteration', 'StopIteration', 'SyntaxError', 'SyntaxWarning',
                'SystemError', 'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError',
                'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError',
                'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning',
                'WindowsError', 'ZeroDivisionError']

BUILD_IN_FUNC = ['abs', 'all', 'any', 'ascii', 'bin', 'bool', 'eval', 'exec', 'input', 'raw_input',
                'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex',
                'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate',
                'exit', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help',
                'hex', 'id', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'license',
                'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct',
                'ord', 'pow', 'print', 'property', 'quit', 'range', 'repr', 'reversed', 'round', 'set', 'setattr',
                'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip', '__import__',
                 'reload']


BUILD_IN_VAR = ['__build_class__', '__debug__', '__doc__', '__import__',
                '__loader__', '__name__', '__package__', '__spec__']

BUILD_IN_STR_METHOD = ['capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find', 'format',
                       'format_map', 'index', 'isalnum', 'isalpha', 'isascii', 'isdecimal', 'isdigit', 'isidentifier', 'islower',
                       'isnumeric', 'isprintable', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'partition',
                       'removeprefix', 'removesuffix', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip',
                       'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']

BUILD_IN_DICT_METHOD = ['get', 'items', 'keys', 'pop', 'popitem', 'reversed', 'setdefault', 'update', 'values']

BUILD_IN_PASS_METHOD = ['append', 'update']

BUILD_IN_FILE_IO = ['read', 'write']

BUILD_IN_MODEL_FUNC = ['os.path.abspath', 'os.path.basename', 'os.path.commonpath', 'os.path.commonprefix', 'os.path.dirname',
                       'os.path.exists', 'os.path.lexists', 'os.path.expanduser', 'os.path.expandvars', 'os.path.getatime',
                       'os.path.getmtime', 'os.path.getctime', 'os.path.getsize', 'os.path.isabs', 'os.path.isfile', 'os.path.isdir',
                       'os.path.islink', 'os.path.ismount', 'os.path.join', 'os.path.normcase', 'os.path.normpath', 'os.path.realpath',
                       'os.path.relpath', 'os.path.samefile', 'os.stat', 'os.path.sameopenfile', 'os.path.samestat', 'os.path.split',
                       'os.path.splitdrive', 'os.path.splitext', 'os.path.supports_unicode_filenames']

SPECIAL_FUNC = ['MAKE_FUNCTION']

