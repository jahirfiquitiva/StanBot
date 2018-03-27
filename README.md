# Stan Bot

Stan Bot is a simple (really simple) bot that listens to user messages and replies with question to complete a simple SCRUM stand up.

This bot uses the [Simple-Slack-Bot library](https://github.com/GregHilston/Simple-Slack-Bot) and also the official [Python Slack Client](https://github.com/slackapi/python-slackclient)

## Use

Stan replies to these "commands":

`stan min`:
Starts a minimal stand-up. For reports at the end of the day, basically.
The questions are:
* What did you do today?
* Are there any obstacles impeding your progress?

`stan full`:
Starts a full stand-up. For reports at the beginning of the day, basically.
* What did you do yesterday?
* What are you going to do today?
* Are there any obstacles impeding your progress?

## Deployment on Heroku

* Fork the project
* Create a [Heroku](https://dashboard.heroku.com/) app
* Create a [Slack bot user](https://my.slack.com/apps/A0F7YS25R-bots) and get its API Token
* Configure an environment variable on Heroku with key: `SLACK_BOT_TOKEN` and the bot API Token as its value.
* Connect the app with the GitHub repository
* On your app management page, configure the dyno and set it on.
* Trigger deployment

## Contribution

This project is far from perfect and could have a lot of useful features. I am by no means an expert on bots creation: this is literally my first attempt

I am open to any kind of contributions (pull-requests) that can help Stan grow and become more powerful :)

Thanks in advance for them
