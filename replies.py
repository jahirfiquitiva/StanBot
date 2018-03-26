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
        mm = 2 if simple else 3
        print("Current replies: " + str(self.count()))
        if self.count() > mm:
            self.replies = []
            self.active = False
            return True
        return False

    def activate(self, active=True):
        self.active = active
