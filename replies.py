class Replies:
    def __init__(self):
        self.replies = []
        self.active = False

    def count(self):
        return len(self.replies)

    def reply(self, message, simple=False):
        if not self.active:
            return True
        self.replies.append(message)
        max = 2 if simple else 3
        if self.count() > max:
            self.replies = []
            self.active = False
            return True
        return False

    def activate(self):
        self.active = True
