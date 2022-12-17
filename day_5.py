import factory_day5

DATAS_DAY5_URL = "https://adventofcode.com/2022/day/5/input"


def day5():
    datas = factory_day5.Moves(DATAS_DAY5_URL)

    datas.load_datas()
    print(f"before: {datas.warehouse.elves_message}")
    datas.warehouse.do_transfer()
    print(f"after: {datas.warehouse.elves_message}")
