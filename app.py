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
        stan.get_slacker().chat.post_message(request.channel, "hola")


def main():
    stan.start()


if __name__ == "__main__":
    main()
