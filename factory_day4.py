import os
import re

import requests

SESSION_COOKIE = os.environ["SESSION_COOKIE"]
COOKIES = {"session": SESSION_COOKIE}
HEADERS = {"User-Agent": "USER_AGENT"}

DATAS_DAY4_URL = "https://adventofcode.com/2022/day/4/input"


def day4():
    pairs = Pairs(DATAS_DAY4_URL)

    pairs.load_pairs()
    print(
        f"The number of paris totally overlap is: {pairs.how_many_assignement_pairs_is_totally_overlap}"
    )
    print(
        f"The number of paris totally overlap is: {pairs.how_many_assignement_pairs_is_partial_overlap}"
    )


class Elf(object):
    def __init__(self, begin_section, end_section):
        self.begin_section = begin_section
        self.end_section = end_section


class Pair(object):
    def __init__(self, elf_one: Elf, elf_two: Elf):
        self.elf_one = elf_one
        self.elf_two = elf_two

    @property
    def is_sections_one_is_partial_overloop_by_two(self):
        return (
            (self.elf_one.begin_section >= self.elf_two.begin_section)
            and (self.elf_one.begin_section <= self.elf_two.end_section)
        ) or (
            (self.elf_one.end_section >= self.elf_two.begin_section)
            and (self.elf_one.end_section <= self.elf_two.end_section)
        )

    @property
    def is_sections_two_is_partial_overloop_by_one(self):
        return (
            (self.elf_two.begin_section >= self.elf_one.begin_section)
            and (self.elf_two.begin_section <= self.elf_one.end_section)
        ) or (
            (self.elf_two.end_section >= self.elf_one.begin_section)
            and (self.elf_two.end_section <= self.elf_one.end_section)
        )

    @property
    def is_sections_one_is_into_sections_two(self):
        return (self.elf_one.begin_section >= self.elf_two.begin_section) and (
            self.elf_one.end_section <= self.elf_two.end_section
        )

    @property
    def is_sections_two_is_into_sections_one(self):
        return (self.elf_two.begin_section >= self.elf_one.begin_section) and (
            self.elf_two.end_section <= self.elf_one.end_section
        )

    @property
    def is_totally_overlap(self):
        return (
            self.is_sections_one_is_into_sections_two
            or self.is_sections_two_is_into_sections_one
        )

    @property
    def is_partial_overlap(self):
        return (
            self.is_sections_two_is_partial_overloop_by_one
            or self.is_sections_one_is_partial_overloop_by_two
        )


class Pairs(object):
    def __init__(self, url_to_load):
        self.url_to_load = url_to_load
        self.pairs = []

    def add_pair(self, pair):
        self.pairs.append(pair)

    def load_pairs(self):
        request_to_load = requests.get(
            self.url_to_load, cookies=COOKIES, headers=HEADERS
        )
        pairs_text = request_to_load.text.replace(" ", "-")
        for pair_text in pairs_text.split(sep=None):
            sections_limit = re.match("(\d+)-(\d+),(\d+)-(\d+)", pair_text)  # noqa
            begin_section_of_first_elf = int(sections_limit.group(1))
            end_section_of_first_elf = int(sections_limit.group(2))
            begin_section_of_second_elf = int(sections_limit.group(3))
            end_section_of_second_elf = int(sections_limit.group(4))
            elf_one = Elf(begin_section_of_first_elf, end_section_of_first_elf)
            elf_two = Elf(begin_section_of_second_elf, end_section_of_second_elf)
            self.pairs.append(Pair(elf_one, elf_two))

            print(
                f"1:{begin_section_of_first_elf} to {end_section_of_first_elf}/ 2:{begin_section_of_second_elf} to {end_section_of_second_elf} "
            )

    @property
    def how_many_assignement_pairs_is_totally_overlap(self):
        number_pairs = 0
        for pair in self.pairs:
            if pair.is_totally_overlap:
                number_pairs += 1

        return number_pairs

    @property
    def how_many_assignement_pairs_is_partial_overlap(self):
        number_pairs = 0
        for pair in self.pairs:
            if pair.is_partial_overlap:
                number_pairs += 1

        return number_pairs
