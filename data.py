from typing import Final, Literal, TypeAlias

Item: TypeAlias = Literal["a", "b", "c", "d", "e", "f"]
BrandItem: TypeAlias = Literal["Crab", "Milk", "Cheese", "Bread", "Apple", "Pie"]
ItemCombo: TypeAlias = frozenset[BrandItem]

q1_database: Final[dict[int, set[Item]]] = {
    1: {"a", "b", "c", "d"},
    2: {"b", "c", "e", "f"},
    3: {"a", "d", "e", "f"},
    4: {"a", "e", "f"},
    5: {"b", "d", "f"},
}

q2_database: Final[dict[int, set[BrandItem]]] = {
    1: {"Crab", "Milk", "Cheese", "Bread"},
    2: {"Cheese", "Milk", "Apple", "Pie", "Bread"},
    3: {"Apple", "Crab", "Pie", "Bread"},
    4: {"Bread", "Milk", "Cheese"},
}
