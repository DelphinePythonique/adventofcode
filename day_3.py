import factory_day3

DATAS_DAY3_URL = "https://adventofcode.com/2022/day/3/input"


def day3():
    rucksacks = factory_day3.Rucksacks(DATAS_DAY3_URL)
    rucksacks.load_rucksacks()
    print(f"total sum_prioruties is: {rucksacks.sum_priorities}")
