DATAS_DAY1_URL = "https://adventofcode.com/2022/day/1/input"


def day1():
    import factory_day1

    elves_team = factory_day1.ElvesTeam(DATAS_DAY1_URL)
    elves_team.load_elves()
    print(
        f"Elf with max calories has : {elves_team.max_calories_among_elves(1)} calories"
    )
    print(
        f"the three first Elves with max calories has : {elves_team.max_calories_among_elves(3)} calories"
    )
