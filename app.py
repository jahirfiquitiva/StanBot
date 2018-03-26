import os
from simple_slack_bot.simple_slack_bot import SimpleSlackBot
from slackclient import SlackClient

stan = SimpleSlackBot(debug=True)
sc = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))


@stan.register("message")
def pong_callback(request):
    """This function is called every time a message is sent to a channel out Bot is in

    :param request: the SlackRequest we receive along with the event. See the README.md for full documentation
    :return: None
    """
    if request.message.lower() == "ping":
        request.write("Pong")
    if request.message.lower() == "stan-up!":
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
        dail = {
            "callback_id": "ryde-46e2b0",
            "title": "Request a Ride",
            "submit_label": "Request",
            "elements": [
                {
                    "type": "text",
                    "label": "Pickup Location",
                    "name": "loc_origin"
                },
                {
                    "type": "text",
                    "label": "Dropoff Location",
                    "name": "loc_destination"
                }
            ]
        }
        sc.api_call(
            "dialog.open",
            channel=request.channel,
            trigger_id="my.trigger",
            dialog=dail
        )
    if request.message.lower() == "thread":
        sc.api_call(
            "chat.postMessage",
            channel=request.channel,
            text="Thread from Python! :tada:",
            thread_ts="1476746830.000003",
            reply_broadcast=True
        )


def main():
    stan.start()


if __name__ == "__main__":
    main()
