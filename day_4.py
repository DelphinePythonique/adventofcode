import factory_day4

DATAS_DAY4_URL = "https://adventofcode.com/2022/day/4/input"


def day4():
    pairs = factory_day4.Pairs(DATAS_DAY4_URL)

    pairs.load_pairs()
    print(f"The number of paris totally overlap is: {pairs.how_many_assignement_pairs_is_totally_overlap}")
