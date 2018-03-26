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

    def activate(self, active=True):
        if not active:
            self.replies = []
        self.active = active

    def get_as_attachment(self):
        return [
            {
                "title": "What did you do yesterday?",
                "text": self.replies[0],
                "color": "#26de81",
                "attachment_type": "default"
            },
            {
                "title": "What will you do today?",
                "text": self.replies[1],
                "color": "#4b7bec",
                "attachment_type": "default"
            },
            {
                "title": "What's blocking you?",
                "text": self.replies[2],
                "color": "#eb3b5a",
                "attachment_type": "default"
            }
        ]
