from slackbot.bot import listen_to, respond_to

import slackbot_settings as ss


@respond_to("うるせえ")
def mention_func(message):
    message.reply("そんなこと言わないで……")


@respond_to("写真")
def picture(message):
    import cv2 as cv
    import requests
    import datetime
    import os.path

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
        "token": ss.API_TOKEN,
        "channels": ss.CHANNEL_ID,
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

    if jsonfile["forecasts"][0]["temperature"]["min"] is not None:
        min = jsonfile["forecasts"][0]["temperature"]["min"]["celsius"]
    else:
        min = "null"

    if jsonfile["forecasts"][0]["temperature"]["max"] is not None:
        max = jsonfile["forecasts"][0]["temperature"]["max"]["celsius"]
    else:
        max = "null"

    description_min = "最低気温は " + min + "℃" + "\n"
    description_max = "最高気温は " + max + "℃" + "\n"

    message.send("今日の天気予報です")
    message.send("\n" + description_min + description_max + "\n" + text)


@respond_to("ダウンロード")
def download_file(message):
    from libs.download import DownloadFile

    file_types = ["jpg", "png", "pdf", "zip"]
    save_path = "../Downloads/"

    download_file = DownloadFile(file_types, save_path)
    result = download_file.exe_download(message._body["files"][0])
    if result == "ok":
        message.send("ファイルをダウンロードしました")
    elif result == "file type is not applicable.":
        message.send("ファイルのタイプがダウンロード対象外です")
    else:
        message.send("ファイルのダウンロードに失敗しました")


@respond_to(r"^light\s+\S.*")
def light_switch(message):
    import subprocess
    import shlex

    text = message.body["text"]
    temp, word = text.split(None, 1)

    cmd = "python3 ../irrp.py -p -g17 -f ../codes"
    token = shlex.split(cmd)

    if word == "on":
        token.append("light:on")
        subprocess.run(token)
        message.send("部屋の電気をつけました")
    elif word == "off":
        token.append("light:off")
        subprocess.run(token)
        message.send("部屋の電気を消しました")
    else:
        message.send("```usage: light [on, off]```")


@respond_to(r"^air\s+\S.*")
def air_conditioner(message):
    import subprocess
    import shlex

    text = message.body["text"]
    temp, word = text.split(None, 1)

    cmd = "python3 ../irrp.py -p -g17 -f ../codes"
    token = shlex.split(cmd)

    if word == "heat":
        token.append("heat")
        subprocess.run(token)
        message.send("暖房をつけました")
    elif word == "cool":
        token.append("cool")
        subprocess.run(token)
        message.send("冷房をつけました")
    elif word == "stop":
        token.append("stop")
        subprocess.run(token)
        message.send("エアコンを切りました")
    else:
        message.send("```usage: air [heat, cool, stop]```")


@listen_to("おーい")
def listen_func(message):
    message.send("呼んだ？")
