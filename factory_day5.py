import os
import re
from enum import Enum
from itertools import chain
from typing import List

import requests

SESSION_COOKIE = os.environ["SESSION_COOKIE"]
COOKIES = {"session": SESSION_COOKIE}
HEADERS = {"User-Agent": "USER_AGENT"}


class Stack(object):
    def __init__(self, code):
        self.code = code
        self.crates = []

    def add_crate(self, crate):
        self.crates.append(crate)

    def del_last_crate(self):
        self.crates.pop()


class Warehouse(object):
    def __init__(self):
        self.stacks: List[Stack] = []
        self.moves: List[Move] = []

    def add_stack(self, stack: Stack):
        self.stacks.append(stack)

    def find_stack(self, code):
        return [stack for stack in self.stacks if stack.code == code][0]

    def do_transfer(self):
        for move in self.moves:
            crates_to_transfer = self.extract_crates(move.from_stack, move.quantity)
            move.to_stack.crates.extend(crates_to_transfer)

    @property
    def elves_message(self):
        message = ""
        for stack in self.stacks:
            message += stack.crates[-1]
        return message


    def extract_crates(self, from_stack: Stack, quantity):
        crates_to_transfer = []
        for i in range(0, quantity):
            crates_to_transfer.append(from_stack.crates.pop())
        return crates_to_transfer

class Move(object):
    def __init__(self, quantity, from_stack, to_stack):
        self.quantity = quantity
        self.from_stack: Stack = from_stack
        self.to_stack: Stack = to_stack


class Moves(object):
    def __init__(self, url_to_load):
        self.url_to_load = url_to_load
        self.warehouse = None
        self.moves = []

    def add_move(self, move):
        self.moves.append(move)

    def load_datas(self):
        request_to_load = requests.get(
            self.url_to_load, cookies=COOKIES, headers=HEADERS
        )
        datas_text = request_to_load.text.replace(" ", "-")

        datas_text = datas_text.replace("[", "")
        datas_text = datas_text.replace("]", "")
        print(datas_text)
        # [Q] - --------[N] - ------------[N] - ---
        # [H] - ----[B] - [D] - ------------[S] - [M]
        # [C] - ----[Q] - [J] - --------[V] - [Q] - [D]
        # [T] - ----[S] - [Z] - [F] - ----[J] - [J] - [W]
        # [N] - [G] - [T] - [S] - [V] - ----[B] - [C] - [C]
        # [S] - [B] - [R] - [W] - [D] - [J] - [Q] - [R] - [Q]
        # [V] - [D] - [W] - [G] - [P] - [W] - [N] - [T] - [S]
        # [B] - [W] - [F] - [L] - [M] - [F] - [L] - [G] - [J]
        # -1 - --2 - --3 - --4 - --5 - --6 - --7 - --8 - --9 -
        positions = []
        moves = []
        datas_position = True

        for data_text in datas_text.split(sep=None):
            if data_text[:4] == "-1--":
                datas_position = False
            if datas_position:
                positions_match = re.match(
                    "(\w+|---)-(\w+|---)-(\w+|---)-(\w+|---)-(\w+|---)-(\w+|---)-(\w+|---)-(\w+|---)-(\w+|---)",
                    data_text,
                )
                positions.append(
                    (
                        positions_match.group(1),
                        positions_match.group(2),
                        positions_match.group(3),
                        positions_match.group(4),
                        positions_match.group(5),
                        positions_match.group(6),
                        positions_match.group(7),
                        positions_match.group(8),
                        positions_match.group(9),
                    )
                )

            if data_text[:4] == "move":
                moves_match = re.match(
                    "move-(\d+)-from-(\d+)-to-(\d+)",
                    data_text,
                )
                moves.append(
                    (int(moves_match.group(1)), int(moves_match.group(2)), int(moves_match.group(3)))
                )
        positions.reverse()
        positions_by_stack = list(map(list, zip(*positions)))
        self.populate_warehouse(positions_by_stack)
        self.populate_moves(moves)
        coucou = "that-all"

    def populate_moves(self, moves):
        for move in moves:
            stack_from = self.warehouse.find_stack(move[1])
            stack_to = self.warehouse.find_stack(move[2])
            self.warehouse.moves.append(Move(move[0], stack_from, stack_to))

    def populate_warehouse(self, positions_by_stack):
        self.warehouse = Warehouse()
        for i in range(1, len(positions_by_stack) + 1):
            self.warehouse.add_stack(Stack(i))
            for crate in positions_by_stack[i - 1]:
                if crate != "---":
                    self.warehouse.stacks[i - 1].add_crate(crate)


