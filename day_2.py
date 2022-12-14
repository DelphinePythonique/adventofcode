import factory_day2

DATAS_DAY2_URL = "https://adventofcode.com/2022/day/2/input"


def day2():
    rounds = factory_day2.Rounds(DATAS_DAY2_URL)
    rounds.load_rounds()
    print(f"total gain is: {rounds.gain}")
    rounds.rounds = []
    rounds.load_rounds(factory_day2.round_rule["RULE_RESULT"].value)
    print(f"total gain is: {rounds.gain}")
