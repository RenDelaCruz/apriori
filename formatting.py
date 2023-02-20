from collections.abc import Sequence

from data import ItemCombo


def title(tag: str) -> str:
    title_width = len(tag) + 2

    title_string = f"\n┏{'━' * title_width}┓"
    title_string += f"\n┃ {tag} ┃"
    title_string += f"\n┗{'━' * title_width}┛"
    return title_string


def label(tag: str, padding: int = 2) -> str:
    label_width = 15 + padding

    label_string = (
        f"\n{'•' * label_width}{' ' * padding}{tag}{' ' * padding}{'•' * label_width}\n"
    )
    return label_string


def format_item_combo(item_combo: ItemCombo) -> str:
    return f"{{{', '.join(str(combo) for combo in item_combo)}}}"


def format_table(
    headers: tuple[str, str], data: Sequence[tuple[ItemCombo | str, float]]
) -> str:
    formatted_data = [
        (format_item_combo(key) if isinstance(key, frozenset) else key, f"{value:0.2f}")
        for key, value in data
    ]
    max_left_column_size = max(
        len(row) for row in [line[0] for line in formatted_data] + [headers[0]]
    )
    max_right_column_size = max(
        len(row) for row in [line[1] for line in formatted_data] + [headers[1]]
    )

    table_string = f"\n┌{'─' * (max_left_column_size + 1)}─┬─{'─' * (max_right_column_size + 1)}┐\n"
    table_string += f"│ {headers[0]:<{max_left_column_size}} │ {headers[1]:<{max_right_column_size}} │\n"
    table_string += (
        f"├{'─' * (max_left_column_size + 1)}─┼─{'─' * (max_right_column_size + 1)}┤\n"
    )

    for key, value in formatted_data:
        table_string += (
            f"│ {key:<{max_left_column_size}} │ {value:<{max_right_column_size}} │\n"
        )

    table_string += (
        f"└{'─' * (max_left_column_size + 1)}─┴─{'─' * (max_right_column_size + 1)}┘\n"
    )
    return table_string
