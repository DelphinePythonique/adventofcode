import os
import re
from enum import Enum

import requests

SESSION_COOKIE = os.environ["SESSION_COOKIE"]
COOKIES = {"session": SESSION_COOKIE}
HEADERS = {"User-Agent": "USER_AGENT"}


class type_object(Enum):
    A, X = "ROCK", "ROCK"
    B, Y = "PAPER", "PAPER"
    C, Z = "SCISSOR", "SCISSOR"


class type_object_gain(Enum):
    ROCK = 1
    PAPER = 2
    SCISSOR = 3


class amount_gain_by_result(Enum):
    LOSS = 0
    EQ = 3
    WIN = 6


class combinaison_result(Enum):
    ROCKROCK, PAPERPAPER, SCISSORSCISSOR = "EQ", "EQ", "EQ"
    ROCKPAPER, SCISSORROCK, PAPERSCISSOR = "WIN", "WIN", "WIN"
    PAPERROCK, ROCKSCISSOR, SCISSORPAPER = "LOSS", "LOSS", "LOSS"


class Round(object):
    def __init__(self, opponent_choice, my_choice):

        self.opponent_choice = opponent_choice
        self.my_choice = my_choice

    @property
    def opponent_object(self):
        return type_object[self.opponent_choice].value

    @property
    def my_object(self):
        return type_object[self.my_choice].value

    @property
    def result(self):
        combinaison = f"{self.opponent_object}{self.my_object}"
        return combinaison_result[combinaison].value

    @property
    def gain(self):
        return (
            amount_gain_by_result[self.result].value
            + type_object_gain[self.my_object].value
        )


class Rounds(object):
    def __init__(self, url_to_load):
        self.url_to_load = url_to_load
        self.rounds = []

    def add_round(self, round):
        self.rounds.append(round)

    def load_rounds(self):
        request_to_load = requests.get(
            self.url_to_load, cookies=COOKIES, headers=HEADERS
        )
        rounds_text = request_to_load.text.replace(" ", "-")
        for round_text in rounds_text.split(sep=None):
            round_participants = re.match("(\w+)-(\w+)", round_text)

            new_round = Round(round_participants.group(1), round_participants.group(2))
            self.rounds.append(new_round)
            print(
                f"{round_participants.group(1)}--{round_participants.group(2)}/{new_round.opponent_object}--{new_round.my_object}=>{new_round.result}/gain = {new_round.gain}"
            )

    @property
    def gain(self):
        gain = 0
        for round in self.rounds:
            gain += round.gain
        return gain