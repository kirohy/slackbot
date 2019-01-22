from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply
import os.path
import slackbot_settings
import datetime
import cv2 as cv
import requests

@respond_to('うるせえ')
def mention_func(message):
    message.reply('だまれ')

@respond_to('写真')
def picture(message):
    cap = cv.VideoCapture(0)
    cap.set(3,160)
    cap.set(4,120)

    ref, img = cap.read()

    date = datetime.datetime.now()
    filename = date.strftime('%Y-%m-%d-%H:%M:%S.jpg')
    path = os.path.join('../Pictures', filename)

    cv.imwrite(path, img)

    cap.release()
    cv.destroyAllWindows()

    files = {'file': open(path, 'rb')}
    param = {
        'token': slackbot_settings.API_TOKEN,
        'channels': slackbot_settings.CHANNEL_ID,
        'filename': filename,
        'initial_comment': '写真を撮影しました',
        'title': filename
    }
    requests.post(url='https://slack.com/api/files.upload',params=param, files=files)



@listen_to('おーい')
def listen_func(message):
    message.send('呼んだ？')
