import os
import replies
import datetime
from simple_slack_bot.simple_slack_bot import SimpleSlackBot
from slackclient import SlackClient

# Put # before name if it's a public channel. Make sure your bot is a channel member
REPORTS_CHANNEL = "frames"

# This is the link of the repo where the bot code is available (Make sure it doesn't end with "/" )
BOT_REPO_URL = "https://github.com/jahirfiquitiva/StanBot"

stan = SimpleSlackBot()
sc = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))
reps = replies.Replies()

simple_mess = [
    "What did you do today?",
    "Are there any obstacles impeding your progress?"
]

detail_mess = [
    "What did you do yesterday?",
    "What are you going to do today?",
    "Are there any obstacles impeding your progress?"
]


@stan.register("message")
def callback(request):
    if reps.active and len(request.message) > 0:
        reps.reply(request.message)
        mm = 2 if reps.simple else 3
        if reps.count() < mm:
            sc.api_call(
                "chat.postMessage",
                channel=request.channel,
                text=simple_mess[reps.count()] if reps.simple else detail_mess[reps.count()])
        else:
            sc.api_call(
                "chat.postMessage",
                channel=request.channel,
                text="Your stand-up is finished :smile:")

            offset = stan.helper_user_id_to_tz_offset(request.user)
            ft = datetime.datetime.fromtimestamp(request.timestamp + offset).strftime(
                '%Y-%m-%d %H:%M:%S')

            sc.api_call(
                "chat.postMessage",
                channel=REPORTS_CHANNEL,
                text="Here's *" + stan.helper_user_id_to_user_real_name(
                    request.user) + "*'s report at *" + ft + "*:",
                attachments=reps.get_as_attachment(),
                mrkdwn=True
            )
            reps.deactivate()
    elif request.message.lower() == "stan min":
        start_stan(True, request.channel)
    elif request.message.lower() == "stan full":
        start_stan(False, request.channel)
    else:
        button = [
            {
                "actions": [
                    {
                        "type": "button",
                        "text": "Report on GitHub",
                        "url": BOT_REPO_URL + "/issues/new",
                        "style": "primary"
                    }
                ]
            }
        ]
        sc.api_call(
            "chat.postMessage",
            channel=request.channel,
            text="Sorry, I'm not that smart yet :disappointed:",
            attachments=button)


def start_stan(simple, chan):
    reps.activate(simple)
    message = simple_mess[reps.count()] if simple else detail_mess[reps.count()]
    sc.api_call(
        "chat.postMessage",
        channel=chan,
        text="Let's start your stand up! :thinking_face:\n" + message)


def main():
    stan.start()


if __name__ == "__main__":
    main()
