from simple_slack_bot.simple_slack_bot import SimpleSlackBot

stan = SimpleSlackBot(debug=True)


@stan.register("message")
def pong_callback(request):
    """This function is called every time a message is sent to a channel out Bot is in

    :param request: the SlackRequest we receive along with the event. See the README.md for full documentation
    :return: None
    """
    if request.message.lower() == "ping":
        request.write("Pong")
    if request.message.lower() == "mes":
        att = [
            {
                "text": "Choose a game to play",
                "fallback": "You are unable to choose a game",
                "callback_id": "wopr_game",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "game",
                        "text": "Chess",
                        "type": "button",
                        "value": "chess"
                    },
                    {
                        "name": "game",
                        "text": "Falken's Maze",
                        "type": "button",
                        "value": "maze"
                    },
                    {
                        "name": "game",
                        "text": "Thermonuclear War",
                        "style": "danger",
                        "type": "button",
                        "value": "war",
                        "confirm": {
                            "title": "Are you sure?",
                            "text": "Wouldn't you prefer a good game of chess?",
                            "ok_text": "Yes",
                            "dismiss_text": "No"
                        }
                    }
                ]
            }]
        stan.get_slacker().chat.post_message(request.channel,
                                             "hola",
                                             attachments=att)


def main():
    stan.start()


if __name__ == "__main__":
    main()
