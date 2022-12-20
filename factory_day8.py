import os
import requests

SESSION_COOKIE = os.environ["SESSION_COOKIE"]
COOKIES = {"session": SESSION_COOKIE}
HEADERS = {"User-Agent": "USER_AGENT"}


DATAS_DAY8_URL = "https://adventofcode.com/2022/day/8/input"


def day8():
    datas = Stream(DATAS_DAY8_URL)

    datas.load_datas()
    print(f"{datas.count_visible_tree()} visibles trees")
    print(datas.sorted_tree_by_scenic_score())


class Tree(object):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.visible = None
        self.scenic_score = 0

    def __repr__(self):
        return f"x:{self.x}- y:{self.y} - size:{self.size} - scenic score:{self.scenic_score}"


class Stream(object):
    def __init__(self, url_to_load):
        self.url_to_load = url_to_load
        self.trees = []
        self.grid = []
        self.grid_transpose = []

    def sorted_tree_by_scenic_score(self):
        return sorted(self.trees, key=lambda x: x.scenic_score)

    def tree_is_visible(self, tree: Tree):
        if tree.x in (0, len(self.grid[0]) - 1) or tree.y in (0, len(self.grid) - 1):
            print(f"tree:  {tree} cause edge")
            tree.visible = True
            return True
        # left_control:
        max_left = max(self.grid[tree.y][0 : tree.x])
        if tree.size > max_left:
            print(f"tree:  {tree} visible by left max_left is {max_left}")
            tree.visible = True
            return True

        # right_control
        max_right = max(self.grid[tree.y][tree.x + 1 :])
        if tree.size > max_right:
            print(f"tree:  {tree} visible right max_right is {max_right}")
            tree.visible = True
            return True

        # top_control:
        max_top = max(self.grid_transpose[tree.x][0 : tree.y])
        if tree.size > max_top:
            print(f"tree:  {tree} visible by top max_top is {max_top}")
            tree.visible = True
            return True

        # right_control
        max_bottom = max(self.grid_transpose[tree.x][tree.y + 1 :])
        if tree.size > max_bottom:
            print(f"tree:  {tree} visible bottom max_bottom is {max_bottom}")
            tree.visible = True
            return True

        print(f"tree:  {tree} not visible ")
        return False

    def load_datas(self):
        request_to_load = requests.get(
            self.url_to_load, cookies=COOKIES, headers=HEADERS
        )
        datas_text = request_to_load.text.replace(" ", "-")
        lines_str = datas_text.split(sep=None)
        lines = []
        for line in lines_str:
            line_number = list(map(int, line))
            lines.append(line_number)
        print(f"tableau de {len(lines)} lines and {len(lines[0])} columns")
        print(lines[0][0])
        max_line = len(lines)
        max_column = len(lines[0])
        self.grid = lines
        self.grid_transpose = list(zip(*lines))
        for y in range(0, max_line):
            for x in range(0, max_column):
                self.trees.append(Tree(x, y, lines[y][x]))
        self.populate_visible_tree_attribute()
        self.populate_scenic_score()

    def populate_visible_tree_attribute(self):
        count_visible_tree = 0
        for tree in self.trees:
            if self.tree_is_visible(tree):

                count_visible_tree += 1

    def count_visible_tree(self):
        count_visible_tree = 0
        for tree in self.trees:
            if tree.visible:
                count_visible_tree += 1
        return count_visible_tree

    def populate_scenic_score(self):
        for tree in self.trees:
            self.calculate_scenic_score(tree)

    def calculate_scenic_score(self, tree):
        if tree.x in (0, len(self.grid[0]) - 1) or tree.y in (0, len(self.grid) - 1):
            tree.scenic_score = 0
            print(f"tree:  {tree} -  cause edge")
            return tree.scenic_score

        # left_control:
        score_left = 0
        for neighboring_tree_size in reversed(self.grid[tree.y][0 : tree.x]):
            score_left += 1
            if neighboring_tree_size >= tree.size:
                break
        print(f"tree:  {tree} visible score_left is {score_left}")

        # right_control
        score_right = 0
        for neighboring_tree_size in self.grid[tree.y][tree.x + 1 :]:
            score_right += 1
            if neighboring_tree_size >= tree.size:
                break
        print(f"tree:  {tree} -  score_right is {score_right}")

        # top_control:
        score_top = 0
        for neighboring_tree_size in reversed(self.grid_transpose[tree.x][0 : tree.y]):
            score_top += 1

            if neighboring_tree_size >= tree.size:
                break
        print(f"tree:  {tree} score_top is {score_top}")

        # bottom_control
        score_bottom = 0
        for neighboring_tree_size in self.grid_transpose[tree.x][tree.y + 1 :]:
            score_bottom += 1
            if neighboring_tree_size >= tree.size:
                break
        print(f"tree:  {tree} score_bottom is {score_bottom}")

        tree.scenic_score = score_top * score_right * score_left * score_bottom
        return tree.scenic_score
