

class Utils:
    def __init__(self):
        self.insts_stack = []

    def stack_push(self, inst):
        self.insts_stack.append(inst)

    def stack_pop(self):
        if self.insts_stack:
            inst = self.insts_stack.pop()
            return inst
        else:
            return None

    def stack_clean(self):
        self.insts_stack = []