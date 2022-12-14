import os

import requests

SESSION_COOKIE = os.environ["SESSION_COOKIE"]
COOKIES = {"session": SESSION_COOKIE}
HEADERS = {"User-Agent": "USER_AGENT"}


class Rucksack(object):
    def __init__(self, letters_list):
        self.letters_list = letters_list

    @property
    def found_letter(self):
        found_letter =  set(self.letters_list[0]) & set(self.letters_list[1])
        return list(found_letter)[0]


    @property
    def priority(self):
        # a: 97
        # z: 122
        # A: 65
        # Z: 90
        ord_code = ord(self.found_letter)
        if 96 < ord_code < 123:
            return ord_code - 96
        if 64 < ord_code < 91:
            return ord_code - 38

        return 0


class Rucksacks(object):
    def __init__(self, url_to_load):
        self.url_to_load = url_to_load
        self.rucksacks = []

    def add_round(self, round):
        self.rucksacks.append(round)

    def load_rucksacks(self):
        request_to_load = requests.get(
            self.url_to_load, cookies=COOKIES, headers=HEADERS
        )
        rucksacks_text = request_to_load.text.replace(" ", "-")
        print("=" * 20)

        for rucksack_text in rucksacks_text.split(sep=None):
            letters_list = []
            letters_list.append(rucksack_text[:int(len(rucksack_text) / 2)])
            letters_list.append(rucksack_text[int(len(rucksack_text) / 2):int(len(rucksack_text))])

            new_rucksack = Rucksack(letters_list)
            self.rucksacks.append(new_rucksack)
            print(f"{rucksack_text}:-{new_rucksack.found_letter}-{new_rucksack.priority}")

    @property
    def sum_priorities(self):
        sum_priorities = 0
        for rucksack in self.rucksacks:
            sum_priorities += rucksack.priority
        return sum_priorities
