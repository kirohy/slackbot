import datetime
import os.path

import cv2 as cv
import requests
from slackbot.bot import listen_to, respond_to

import slackbot_settings


@respond_to("うるせえ")
def mention_func(message):
    message.reply("だまれ")


@respond_to("写真")
def picture(message):
    cap = cv.VideoCapture(0)
    cap.set(3, 160)
    cap.set(4, 120)

    ref, img = cap.read()

    date = datetime.datetime.now()
    filename = date.strftime("%Y-%m-%d-%H:%M:%S.jpg")
    path = os.path.join("../Pictures", filename)

    cv.imwrite(path, img)

    cap.release()
    cv.destroyAllWindows()

    upload = "https://slack.com/api/files.upload"
    file = {"file": open(path, "rb")}
    param = {
        "token": slackbot_settings.API_TOKEN,
        "channels": slackbot_settings.CHANNEL_ID,
        "filename": filename,
        "initial_comment": "写真を撮影しました",
        "title": filename,
    }
    requests.post(url=upload, params=param, files=file)


@respond_to("天気")
def weather(message):
    import json
    import urllib.response

    url = "http://weather.livedoor.com/forecast/webservice/json/v1?city=130010"
    response = urllib.request.urlopen(url)
    jsonfile = json.loads(response.read().decode("utf-8"))
    text = jsonfile["description"]["text"]
    min = jsonfile["forecasts"][0]["temperature"]["min"]["celsius"]
    max = jsonfile["forecasts"][0]["temperature"]["max"]["celsius"]

    description_min = "最低気温は " + min + "℃" + "\n"
    description_max = "最高気温は " + max + "℃" + "\n"

    message.reply(description_min + description_max + "\n" + text)


@listen_to("おーい")
def listen_func(message):
    message.send("呼んだ？")
