from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply

@respond_to('うるせえ')
def mention_func(message):
    message.reply('だまれ')

@listen_to('Robotech')
def listen_func(message):
    message.send('RoboTech')
