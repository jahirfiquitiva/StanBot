class Replies:
    def __init__(self):
        self.count = 0
        self.replies = []
        self.active = False

    def reply(self, message, simple=False):
        if not self.active:
            return True
        self.replies[self.count] = message
        self.count += 1
        max = 2 if simple else 3
        if self.count > max:
            self.replies = []
            self.count = 0
            self.active = False
            return True
        return False

    def activate(self):
        self.active = True
