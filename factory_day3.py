import os
from enum import Enum
from itertools import chain

import requests

SESSION_COOKIE = os.environ["SESSION_COOKIE"]
COOKIES = {"session": SESSION_COOKIE}
HEADERS = {"User-Agent": "USER_AGENT"}


class rule(Enum):
    RULE_DIVIDE_RUCKSACK_BY_2 = 1  # compare 2 half rucksacks
    RULE_THREE_RUCKSACS = 2  # compare 3 rucksacks


class Rucksack(object):
    def __init__(self, letters_list):
        self.letters_list = letters_list

    @property
    def found_letter(self):
        list_number = len(self.letters_list)

        found_letters = set(chain.from_iterable(self.letters_list))

        i = 1
        while i < list_number:
            found_letters = (
                found_letters
                & set(self.letters_list[i - 1])
                & set(self.letters_list[i])
            )
            i += 1

        return list(found_letters)[0]

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

    def add_rucksack(self, rucksack):
        self.rucksacks.append(rucksack)

    def load_rucksack_with_rule_divide_by_two(self, rucksacks_text):
        for rucksack_text in rucksacks_text.split(sep=None):
            letters_list = []
            letters_list.append(rucksack_text[: int(len(rucksack_text) / 2)])
            letters_list.append(
                rucksack_text[int(len(rucksack_text) / 2) : int(len(rucksack_text))]
            )

            new_rucksack = Rucksack(letters_list)
            self.rucksacks.append(new_rucksack)
            print(
                f"{rucksack_text}:-{new_rucksack.found_letter}-{new_rucksack.priority}"
            )

    def load_rucksacks(self, choice_rule=rule["RULE_DIVIDE_RUCKSACK_BY_2"].value):
        request_to_load = requests.get(
            self.url_to_load, cookies=COOKIES, headers=HEADERS
        )
        rucksacks_text = request_to_load.text.replace(" ", "-")
        print("=" * 20)
        if choice_rule == rule["RULE_DIVIDE_RUCKSACK_BY_2"].value:
            self.load_rucksack_with_rule_divide_by_two(rucksacks_text)
        else:
            self.load_rucksack_with_rule_by_three_rucksack(rucksacks_text)

    @property
    def sum_priorities(self):
        sum_priorities = 0
        for rucksack in self.rucksacks:
            sum_priorities += rucksack.priority
        return sum_priorities

    def load_rucksack_with_rule_by_three_rucksack(self, rucksacks_text):
        i = 0
        letters_list = []
        for rucksack_text in rucksacks_text.split(sep=None):

            if i < 3:
                letters_list.append(rucksack_text)
                i += 1
            if i == 3:
                new_rucksack = Rucksack(letters_list)
                self.rucksacks.append(new_rucksack)
                print(
                    f"{rucksack_text}:-{new_rucksack.found_letter}-{new_rucksack.priority}"
                )
                i = 0
                letters_list = []
