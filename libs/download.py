import requests

import slackbot_settings as ss


class DownloadFile:
    def __init__(self, file_types, save_directly):
        self.file_types = file_types
        self.save_directly = save_directly

    def exe_download(self, file_info):

        file_name = file_info["name"]
        url_private = file_info["url_private_download"]

        if file_info["filetype"] in self.file_types:
            self.file_download(url_private, self.save_directly + file_name)
            return "ok"
        else:
            return "file type is not applicable."

    def file_download(self, download_url, save_path):
        img = requests.get(
            download_url,
            allow_redirects=True,
            headers={"Authorization": "Bearer %s" % ss.API_TOKEN},
            stream=True,
        )

        if img.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(img.content)
