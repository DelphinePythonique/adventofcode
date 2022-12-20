import factory_day7

DATAS_DAY7_URL = "https://adventofcode.com/2022/day/7/input"


def day7():
    datas = factory_day7.FileSystem(DATAS_DAY7_URL)

    datas.load_datas()
    directories = datas.sorted_directories_by_size()
    sum_size = 0
    for directory in directories:
        if directory.size <= 100000:
            sum_size += directory.size
            print(f"name: {directory.name} - path: {directory.path} - size: {directory.size}")
    print(f"sum is {sum_size}")

    for directory in directories:
        if directory.size >= 1072511:
            print(f"result: name: {directory.name} - path: {directory.path} - size: {directory.size}")
