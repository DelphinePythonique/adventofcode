import factory_day3

DATAS_DAY3_URL = "https://adventofcode.com/2022/day/3/input"


def day3():
    rucksacks = factory_day3.Rucksacks(DATAS_DAY3_URL)

    rucksacks.load_rucksacks()

    print(f"total sum_prioruties is: {rucksacks.sum_priorities} for rule divide rucksack by 2")
    rucksacks.rucksacks = []
    rucksacks.load_rucksacks(factory_day3.rule["RULE_THREE_RUCKSACS"].value)
    print(f"total sum_prioruties is: {rucksacks.sum_priorities} for rule three rucksacks")
