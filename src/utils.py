

class Utils:
    def __init__(self):
        self.insts_stack = []

    def push(self, inst):
        self.insts_stack.append(inst)

    def pop(self):
        if self.insts_stack:
            inst = self.insts_stack.pop()
            return inst
        else:
            return None

    def clean(self):
        self.insts_stack = []