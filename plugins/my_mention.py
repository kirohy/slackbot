from slackbot.bot import listen_to, respond_to

import slackbot_settings as ss


@respond_to("うるせえ")
def mention_func(message):
    message.reply("そんなこと言わないで……")


@listen_to("写真")
def picture(message):
    import requests
    import datetime
    import os.path
    import shlex
    import subprocess

    date = datetime.datetime.now()
    filename = date.strftime("%Y-%m-%d-%H:%M:%S.jpg")
    path = os.path.join("../Pictures", filename)

    base_cmd = "fswebcam -r 1280x720"
    cmd = shlex.split(base_cmd)
    cmd.append(path)
    subprocess.run(cmd)

    upload = "https://slack.com/api/files.upload"
    file = {"file": open(path, "rb")}
    param = {
        "token": ss.API_TOKEN,
        "channels": ss.CHANNEL_ID,
        "filename": filename,
        "initial_comment": "Successed to take a picture.",
        "title": filename,
    }
    requests.post(url=upload, params=param, files=file)


@listen_to("天気")
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


@listen_to(r"^down\s+\S.*")
def download_file(message):
    from libs.download import DownloadFile
    import shlex

    text = message.body["text"]
    temp, file_path = text.split(None, 1)
    file_types = ["jpg", "png", "pdf", "zip"]
    save_path = file_path

    download_file = DownloadFile(file_types, save_path)
    result = download_file.exe_download(message._body["files"][0])
    if result == "ok":
        message.send("Successed to download a file.")
    elif result == "file type is not applicable.":
        message.send("Error: Invalid filetype")
    else:
        message.send("Failed to download a file.")


@listen_to(r"^up\s+\S.*")
def upload_file(message):
    import os
    import requests
    import shlex

    os.chdir(os.path.abspath(os.path.expanduser("~/mnt/")))

    text = message.body["text"]
    temp, file_path = text.split(None, 1)

    upload = "https://slack.com/api/files.upload"
    file = {"file": open(file_path, "rb")}
    param = {
        "token": ss.API_TOKEN,
        "channels": ss.CHANNEL_ID,
        "initial_comment": "Successed to upload a file.",
    }
    requests.post(url=upload, params=param, files=file)

    os.chdir(os.path.abspath(os.path.expanduser("~/slackbot/")))


@listen_to(r"^cd\s+\S.*")
def shell(message):
    import os
    import subprocess
    import shlex

    os.chdir(os.path.abspath(os.path.expanduser("~/mnt/")))

    text = message.body["text"]
    temp, path = text.split(None, 1)

    os.chdir(os.path.abspath(path))
    current = os.getcwd()
    result = subprocess.check_output("ls")

    message.send(current)
    message.send(result)

    os.chdir(os.path.abspath(os.path.expanduser("~/slackbot/")))


@listen_to(r"^light\s+\S.*")
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


@listen_to(r"^air\s+\S.*")
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
