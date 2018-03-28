import os
import re
import replies
import datetime
from simple_slack_bot.simple_slack_bot import SimpleSlackBot
from slackclient import SlackClient

# Put # before name if it's a public channel. Make sure your bot is a channel member
# You must define REPORTS_CHANNEL key in Heroku
REPORTS_CHANNEL = os.environ.get("REPORTS_CHANNEL")

# This is the link of the repo where the bot code is available (Make sure it doesn't end with "/" )
# You must define BOT_REPO key in Heroku
BOT_REPO_URL = os.environ.get("BOT_REPO")

# Bot name and username
# You must define BOT_NAME key in Heroku
BOT_NAME = os.environ.get("BOT_NAME")

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


@stan.register("app_mention")
def mentions(request):
    callback(request)


@stan.register("message")
def callback(request):
    # noinspection PyBroadException
    try:
        mention = re.search('<@(.+?)>', request.message).group(1)
    except Exception:
        mention = ""

    name = BOT_NAME
    is_mentioned = False
    if len(mention) > 0:
        body = stan.get_slacker().users.info(mention).body["user"]
        name = body["name"]
        real_name = body["real_name"]
        if name == BOT_NAME or real_name == BOT_NAME:
            is_mentioned = True

    if request.message is None or len(request.message) <= 0:
        return

    message = request.message.lower()

    if message == BOT_NAME + " stop" or (is_mentioned and "stop" in message):
        if len(reps.channel) > 0 or reps.active:
            sc.api_call(
                "chat.postMessage",
                channel=reps.channel,
                text="*Your stand-up has been stopped* :face_with_monocle:",
                mrkdwn=True,
                as_user=True)
            reps.deactivate()
        else:
            sc.api_call(
                "chat.postMessage",
                channel=request.channel,
                text="No stand-up is currently in execution :smile:",
                as_user=True)
    else:
        if reps.active and len(request.message) > 0:
            valid = reps.reply(request.channel, request.message)
            if valid:
                mm = 2 if reps.simple else 3
                if reps.count() < mm:
                    sc.api_call(
                        "chat.postMessage",
                        channel=request.channel,
                        text=simple_mess[reps.count()] if reps.simple else detail_mess[
                            reps.count()],
                        as_user=True)
                else:
                    sc.api_call(
                        "chat.postMessage",
                        channel=request.channel,
                        text="*Thanks* :smile: Your stand-up has finished! :raised_hands:",
                        mrkdwn=True,
                        as_user=True)

                    offset = stan.helper_user_id_to_tz_offset(request.user)
                    ft = datetime.datetime.fromtimestamp(request.timestamp + offset).strftime(
                        '%Y-%m-%d %H:%M:%S')

                    sc.api_call(
                        "chat.postMessage",
                        channel=REPORTS_CHANNEL,
                        text=":nerd_face:\nHere's a new report from *" + stan.helper_user_id_to_user_real_name(
                            request.user) + "* made at *" + ft + "* (" +
                             stan.helper_user_id_to_tz_label(request.user) + "):",
                        attachments=reps.get_as_attachment(),
                        mrkdwn=True,
                        as_user=True)
                    reps.deactivate()
            else:
                extra = [{
                    "text": "Please try using `" + BOT_NAME + " min` or `" + BOT_NAME + " full`. Or try again in a few minutes.",
                    "fallback": "Please try using `" + BOT_NAME + " min` or `" + BOT_NAME + " full`.Or try again in a few minutes.",
                    "mrkdwn": True,
                    "color": "#3AA3E3"
                }]
                sc.api_call(
                    "chat.postMessage",
                    channel=request.channel,
                    text="Stan does not seem to be active yet, or someone else is doing a report.",
                    attachments=extra,
                    as_user=True)
        elif message.startswith(BOT_NAME) or message.startswith("@" + BOT_NAME) or is_mentioned:
            # noinspection PyBroadException
            try:
                channel_name = stan.get_slacker().channels.info(request.channel).body["channel"][
                    "name"]
                if channel_name.lower() == REPORTS_CHANNEL.lower():
                    send_dm_message(request)
                    return
                elif channel_name.lower() == REPORTS_CHANNEL[1:].lower():
                    send_dm_message(request)
                    return
            except Exception:
                # noinspection PyBroadException
                try:
                    channel_name = stan.get_slacker().groups.info(request.channel).body["group"][
                        "name"]
                    if channel_name.lower() == REPORTS_CHANNEL.lower():
                        send_dm_message(request)
                        return
                except Exception:
                    pass

            if message == (BOT_NAME + " min") or (is_mentioned and "min" in message):
                start_stan(True, request.channel)
            elif message == (BOT_NAME + " full") or (is_mentioned and "full" in message):
                start_stan(False, request.channel)
            elif ("has joined the channel" in message) and is_mentioned:
                send_message(request,
                             "*Hello there!* I am " + name + ". Thanks for having me here :blush:")
            else:
                button = [{
                    "text": "Please try using `" + BOT_NAME + " min` or `" + BOT_NAME + " full`",
                    "fallback": "Please try using `" + BOT_NAME + " min` or `" + BOT_NAME + " full`",
                    "mrkdwn": True,
                    "color": "#3AA3E3",
                    "actions": [
                        {
                            "type": "button",
                            "text": "Report on GitHub",
                            "url": BOT_REPO_URL + "/issues/new",
                            "style": "danger"
                        }
                    ]
                }]
                sc.api_call(
                    "chat.postMessage",
                    channel=request.channel,
                    text="Sorry, I'm not that smart yet :disappointed:.",
                    attachments=button,
                    mrkdwn=True,
                    as_user=True)


def start_stan(simple, chan):
    reps.activate(chan, simple)
    message = simple_mess[reps.count()] if simple else detail_mess[reps.count()]
    sc.api_call(
        "chat.postMessage",
        channel=chan,
        text="*Let's start your stand-up!* :thinking_face:\n" + message,
        mrkdwn=True,
        as_user=True)


def send_dm_message(request):
    sc.api_call(
        "chat.postMessage",
        channel=request.channel,
        text="I'm not allowed to work here. :confused: Please DM me :grinning:",
        as_user=True)


def send_message(request, message, mrk=False):
    sc.api_call(
        "chat.postMessage",
        channel=request.channel,
        text=message,
        mrdwn=mrk,
        as_user=True)


def main():
    stan.start()
    print(BOT_NAME + " is running now :D")


if __name__ == "__main__":
    main()
    print(BOT_NAME + " is running now :D")
