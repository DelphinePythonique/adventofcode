import os

import requests

SESSION_COOKIE = os.environ["SESSION_COOKIE"]
COOKIES = {"session": SESSION_COOKIE}
HEADERS = {"User-Agent": "USER_AGENT"}


class Food(object):
    def __init__(self, calories: object) -> object:
        self.calories = calories


class Elf(object):
    def __init__(self):
        self.foods = []

    def add_food(self, food):
        self.foods.append(food)

    @property
    def total_of_calories(self):
        return sum(food.calories for food in self.foods)

    def __str__(self):
        return f"elf with {self.total_of_calories}"


class ElvesTeam(object):
    def __init__(self, url_to_load):
        self.url_to_load = url_to_load
        self.elves = []

    def add_elf(self, elf):
        self.elves.append(elf)

    def load_elves(self):
        request_to_load = requests.get(
            self.url_to_load, cookies=COOKIES, headers=HEADERS
        )
        food_text = request_to_load.text.replace("\n\n", "\n-")
        active_elf = Elf()
        self.elves.append(active_elf)
        for food in food_text.split(sep=None):
            if int(food) < 0:
                active_elf = Elf()
                self.elves.append(active_elf)
            active_elf.add_food(Food(abs(int(food))))

    def sort_elves_by_calories(self):
        return self.elves.sort(key=lambda elf: elf.total_of_calories, reverse=True)

    def max_calories_among_elves(self, number_first_elves=1):
        self.sort_elves_by_calories()
        sum_calories = 0
        i = 0
        while i < number_first_elves:
            sum_calories += self.elves[i].total_of_calories
            i += 1
        return sum_calories

    def print_elves(self):
        for elf in self.elves:
            print(f"max: {elf.total_of_calories}")
