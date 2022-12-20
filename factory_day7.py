import operator
import os
import re
from enum import Enum
from typing import List, Dict

import requests

SESSION_COOKIE = os.environ["SESSION_COOKIE"]
COOKIES = {"session": SESSION_COOKIE}
HEADERS = {"User-Agent": "USER_AGENT"}


class TypeNode(Enum):
    FILE = 1
    DIRECTORY = 2


class Node(object):
    def __init__(self, name, path: str, node_type, size=0):
        self.name = name
        self.path = path
        self.size = size
        self.node_type = node_type
        if path in ("", "/"):
            index = f"{path}{name}"
        else:
            index = f"{path}/{name}"
        self.index = index

    def __str__(self):
        return self.index

    def __repr__(self):
        return self.index


class FileSystem(object):
    def __init__(self, url_to_load):
        self.url_to_load = url_to_load
        self.nodes: Dict[str:Node] = {}
        self.if_not_exist_create_dir_or_file("", "/", TypeNode["DIRECTORY"].value)

    def sorted_directories_by_size(self) -> List[Node]:
        directories = [
            node
            for index, node in self.nodes.items()
            if node.node_type == TypeNode["DIRECTORY"].value
        ]
        return sorted(directories, key=operator.attrgetter("size"), reverse=True)

    def display_nodes(self):
        for index, node in self.nodes.items():
            print(
                f" -type: {node.node_type} - index - index: {index} - index: {node.index}  name: {node.name} - path: {node.path} - size: {node.size} "
            )

    def sum_file_nodes_into_path(self, path_plus_name):
        return sum(
            [
                node.size
                for index, node in self.nodes.items()
                if (not re.match(f"^{path_plus_name}", node.path) is None)
                and node.node_type == TypeNode["FILE"].value
            ]
        )

    def if_not_exist_create_dir_or_file(self, path, name, node_type, size=0):
        if path in ("", "/"):
            index = f"{path}{name}"
        else:
            index = f"{path}/{name}"
        if index not in self.nodes.keys():
            self.nodes[index] = Node(name, path, node_type, size)

    def load_datas(self):
        request_to_load = requests.get(
            self.url_to_load, cookies=COOKIES, headers=HEADERS
        )
        datas_text = request_to_load.text.replace(" ", "-")
        pwd = []
        for instruction in datas_text.split(sep=None):

            if instruction[:4] == "$-cd":
                cd_match = re.match("\$-cd-(.*?)$", instruction) # noqa
                directory_name = cd_match.group(1)
                if directory_name not in ("/", ".."):
                    pwd.append(directory_name)
                if directory_name == "/":
                    directory_name = ""
                    pwd.append(directory_name)
                if directory_name == "..":
                    pwd.pop()

                continue
            if instruction[:4] == "$-ls":
                continue
            if instruction[:3] == "dir":
                cd_match = re.match("dir-(.*?)$", instruction)
                directory_name = cd_match.group(1)

                path = "/".join(pwd)
                if path == "":
                    path = "/"
                self.if_not_exist_create_dir_or_file(
                    path, directory_name, TypeNode["DIRECTORY"].value
                )
                continue

            file_match = re.match("(\d+)-(.*?)$", instruction) # noqa
            print(
                f"name file: {file_match.group(2)}- taille: {file_match.group(1)}- pwd: {'/'.join(pwd)}"
            )
            file_name = file_match.group(2)
            path = "/".join(pwd)
            if path == "":
                path = "/"
            size = int(file_match.group(1))
            self.if_not_exist_create_dir_or_file(
                path, file_name, TypeNode["FILE"].value, size
            )
        self.populate_size_of_directories()

        # self.display_nodes()

    def populate_size_of_directories(self):
        directories = [
            node
            for index, node in self.nodes.items()
            if node.node_type == TypeNode["DIRECTORY"].value
        ]
        for directory in directories:
            if directory.path in ("", "/"):
                index = f"{directory.path}{directory.name}"
            else:
                index = f"{directory.path}/{directory.name}"
            directory.size = self.sum_file_nodes_into_path(f"{index}")
