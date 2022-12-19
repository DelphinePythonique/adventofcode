import factory_day8

DATAS_DAY8_URL = "https://adventofcode.com/2022/day/8/input"


def day8():
    datas = factory_day8.Stream(DATAS_DAY8_URL)

    datas.load_datas()
    print(f"{datas.count_visible_tree()} visibles trees")
    coucou = ""

