import factory_day6

DATAS_DAY6_URL = "https://adventofcode.com/2022/day/6/input"


def day6():
    datas = factory_day6.Stream(DATAS_DAY6_URL)

    datas.load_datas()
    print(f"message begin: {datas.begin_of_message(14)}")
