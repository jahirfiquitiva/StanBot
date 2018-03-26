from simple_slack_bot.simple_slack_bot import SimpleSlackBot

simple_slack_bot = SimpleSlackBot(debug=True)


@simple_slack_bot.register("message")
def pong_callback(request):
    """This function is called every time a message is sent to a channel out Bot is in

    :param request: the SlackRequest we receive along with the event. See the README.md for full documentation
    :return: None
    """
    if request.message.lower() == "ping":
        request.write("Pong")


def main():
    simple_slack_bot.start()


if __name__ == "__main__":
    main()
