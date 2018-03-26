class Replies:
    def __init__(self):
        self.replies = []
        self.active = False
        self.simple = False

    def count(self):
        return len(self.replies)

    def reply(self, message):
        if not self.active:
            return False
        mm = 2 if self.simple else 3
        if len(self.replies) >= mm:
            return False
        self.replies.append(message)
        return True

    def activate(self, simple=False):
        self.replies = []
        self.simple = simple
        self.active = True

    def deactivate(self):
        self.replies = []
        self.active = False
        self.simple = False

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
        ] if self.simple else [
            {
                "title": "What did you do today?",
                "text": self.replies[0],
                "color": "#26de81",
                "attachment_type": "default"
            },
            {
                "title": "What's blocking you?",
                "text": self.replies[1],
                "color": "#eb3b5a",
                "attachment_type": "default"
            }
        ]
