import os

import requests

SESSION_COOKIE = os.environ["SESSION_COOKIE"]
COOKIES = {"session": SESSION_COOKIE}
HEADERS = {"User-Agent": "USER_AGENT"}

NUMBER_ITEM_TO_CHECK = 4


class Stream(object):
    def __init__(self, url_to_load):
        self.url_to_load = url_to_load
        self.stream = ""

    def load_datas(self):
        request_to_load = requests.get(
            self.url_to_load, cookies=COOKIES, headers=HEADERS
        )
        datas_text = request_to_load.text.replace(" ", "-")

        datas_text = datas_text.replace("[", "")
        datas_text = datas_text.replace("]", "")
        print(datas_text)
        self.stream = datas_text

    @property
    def begin_of_message(self):
        i = 0
        while i < len(self.stream)-NUMBER_ITEM_TO_CHECK:
            array_to_check = self.stream[i:i+NUMBER_ITEM_TO_CHECK]
            if not self.is_doublon(array_to_check):
                return i + NUMBER_ITEM_TO_CHECK
            i += 1
        return None

    def is_doublon(self, array):
        doublons = [item for item in array if array.count(item) > 1]
        return len(doublons) != 0
