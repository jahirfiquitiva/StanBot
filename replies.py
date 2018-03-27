class Replies:
    def __init__(self):
        self.replies = []
        self.active = False
        self.simple = False
        self.channel = ""

    def count(self):
        return len(self.replies)

    def reply(self, channel, message):
        if not self.active:
            return False
        if len(self.channel) <= 0:
            return False
        if channel != self.channel:
            return False
        mm = 2 if self.simple else 3
        if len(self.replies) >= mm:
            return False
        self.replies.append(message)
        return True

    def activate(self, channel, simple=False):
        self.replies = []
        self.simple = simple
        self.active = True
        self.channel = channel

    def deactivate(self):
        self.replies = []
        self.active = False
        self.simple = False
        self.channel = ""

    def get_as_attachment(self):
        return [
            {
                "title": "What did you do today?",
                "text": self.replies[0],
                "color": "#26de81",
                "attachment_type": "default"
            },
            {
                "title": "Are there any obstacles impeding your progress?",
                "text": self.replies[1],
                "color": "#eb3b5a",
                "attachment_type": "default"
            }
        ] if self.simple else [
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
                "title": "Are there any obstacles impeding your progress?",
                "text": self.replies[2],
                "color": "#eb3b5a",
                "attachment_type": "default"
            }
        ]
