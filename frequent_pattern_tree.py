from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence

from data import Item


class Node:
    def __init__(self, item: Item | None = None) -> None:
        self.item = item
        self.count = 1
        self.nodes: list[Node] = []

    def get_or_attach_item_node(self, item: Item) -> Node:
        for node in self.nodes:
            if item == node.item:
                node.count += 1
                return node

        new_node = Node(item=item)
        self.nodes.append(new_node)
        return new_node

    def pretty_print(
        self,
        level: int = 0,
        is_final_node: bool = False,
        branch_history: set[int] | None = None,
    ) -> str:
        branch_history = branch_history or set()

        tree_string = "{}{}{}\n".format(
            "".join(
                ("│     " if i in branch_history else "      ")
                for i in range(level - 1)
            ),
            ("└────" if is_final_node else "├────") * (level > 0),
            f" {self.item}:{self.count}" if self.item else "root",
        )

        final_node_index = len(self.nodes) - 1
        for index, node in enumerate(self.nodes):
            is_final_node = index == final_node_index

            if is_final_node:
                branch_history.discard(level)
            else:
                branch_history.add(level)

            tree_string += node.pretty_print(
                level=level + 1,
                is_final_node=is_final_node,
                branch_history=branch_history,
            )

        return tree_string

    def __str__(self) -> str:
        return self.pretty_print()


class FrequentPatternTree:
    def __init__(self, data: Sequence[set[Item]], reverse: bool = False) -> None:
        self.root = Node()

        for transaction in data:
            current_node = self.root
            ordered_items = sorted(list(transaction), reverse=reverse)

            for item in ordered_items:
                current_node = current_node.get_or_attach_item_node(item=item)

    def __str__(self) -> str:
        return self.root.__str__()


def get_sorted_item_frequencies(data: Sequence[set[Item]]) -> str:
    frequencies: dict[Item, int] = defaultdict(int)
    for transaction in data:
        for item in transaction:
            frequencies[item] += 1

    sorted_frequencies = sorted(frequencies.items(), key=lambda d: (-d[1], d[0]))
    return f'{{ {", ".join(f"{k}: {v}" for k, v in sorted_frequencies)} }}'
