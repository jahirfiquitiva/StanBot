# Stan Bot

Stan Bot is a simple (really simple) bot that listens to user messages and replies with question to complete a simple SCRUM stand up.

This bot uses the [Simple-Slack-Bot library](https://github.com/GregHilston/Simple-Slack-Bot) and also the official [Python Slack Client](https://github.com/slackapi/python-slackclient)

Stan replies to these "commands":

`stan min`:
Starts a minimal stand-up. For reports at the end of the day, basically.
The questions are:
* What did you do today?
* Is something blocking you?

`stan full`:
Starts a full stand-up. For reports at the beginning of the day, basically.
* What did you do yesterday?
* What are you going to do today?
* Is something blocking you?
