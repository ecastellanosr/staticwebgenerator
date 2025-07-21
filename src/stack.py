class MarkStack:
    def __init__(self, base):
        self.items = []
        self.base = base
    def push(self, item):
        self.items.append(item)

    def size(self):
        return len(self.items)

    def peek(self):
        if len(self.items) == 0:
            return self.base
        return self.items[-1]

    def pop(self):
        if len(self.items) == 0:
            return self.base
        item = self.items[-1]
        del self.items[-1]
        return item