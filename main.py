# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

DATAS_URL = "https://adventofcode.com/2022/day/1/input"

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import factory
    elves_team = factory.ElvesTeam(DATAS_URL)
    elves_team.load_elves()
    print(f"Elf with max calories has : {elves_team.max_calories_among_elves(1)} calories")
    print(f"the three first Elves with max calories has : {elves_team.max_calories_among_elves(3)} calories")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
