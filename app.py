import os
import replies
import datetime
from simple_slack_bot.simple_slack_bot import SimpleSlackBot
from slackclient import SlackClient

stan = SimpleSlackBot()
sc = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))
reps = replies.Replies()

simple_mess = [
    "What did you do today?",
    "Is something blocking you?"
]

detail_mess = [
    "What did you do yesterday?",
    "What are you going to do today?",
    "Is something blocking you?"
]


@stan.register("message")
def pong_callback(request):
    """This function is called every time a message is sent to a channel out Bot is in

    :param request: the SlackRequest we receive along with the event. See the README.md for full documentation
    :return: None
    """
    if reps.active and len(request.message) > 0:
        reps.reply(request.message)
        if reps.count() < 3:
            sc.api_call(
                "chat.postMessage",
                channel=request.channel,
                text=detail_mess[reps.count()])
        else:
            sc.api_call(
                "chat.postMessage",
                channel=request.channel,
                text="Your stand-up is finished :smile:")
            print("Time stamp: " + str(request.timestamp))
            ft = datetime.datetime.fromtimestamp(request.timestamp).strftime('%Y-%m-%d %H:%M:%S')
            print("Formatted time: " + ft)
            print("Frames channel id: " + stan.helper_private_channel_name_to_channel_id("frames"))
            sc.api_call(
                "chat.postMessage",
                channel="#standup",
                text="Here's *" + stan.helper_user_id_to_user_real_name(
                    request.user) + "*'s report:",
                attachments=reps.get_as_attachment(),
                mrkdwn=True
            )
            reps.activate(False)
    if request.message.lower() == "stan sim":
        reps.activate()
        sc.api_call(
            "chat.postMessage",
            channel=request.channel,
            text="Let's start your stand up! :thinking_face:\n" + detail_mess[reps.count()])
    if request.message.lower() == "stannn":
        att = [
            {
                "text": "What kind of stand-up do you want to do?",
                "fallback": "You are unable to do a stand-up",
                "callback_id": "stan-standup",
                "color": "#4b7bec",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "opt",
                        "text": "Simple",
                        "type": "button",
                        "value": "simple"
                    },
                    {
                        "name": "opt",
                        "text": "Complete",
                        "type": "button",
                        "value": "complete"
                    },
                    {
                        "name": "opt",
                        "text": "Cancel",
                        "style": "danger",
                        "type": "button",
                        "value": "cancel",
                        "confirm": {
                            "title": "Are you sure?",
                            "text": "Won't you report anything?",
                            "ok_text": "No",
                            "dismiss_text": "Cancel"
                        }
                    }
                ]
            }]
        stan.get_slacker().chat.post_message(request.channel,
                                             "Let's start with your stand-up! :smile:",
                                             attachments=att)
    if request.message.lower() == "client":
        sc.api_call(
            "chat.postMessage",
            channel=request.channel,
            text="Hello from Python! :tada:"
        )
    if request.message.lower() == "thread":
        channel_message = sc.api_call(
            "chat.postMessage",
            channel="#general",
            text="Let's start the stand-up"
        )

        broadcasted_thread_message = sc.api_call(
            "chat.postMessage",
            channel="#general",
            thread_ts=channel_message['message']['ts'],
            reply_broadcast=True,
            text="A message on a thread, broadcasted to channel. *BUG*, Check my username!"
        )


def main():
    stan.start()


if __name__ == "__main__":
    main()
