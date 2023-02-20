import itertools
from collections import defaultdict
from collections.abc import Sequence

from data import BrandItem, ItemCombo
from formatting import format_item_combo, format_table, label


class Apriori:
    def __init__(
        self,
        data: Sequence[set[BrandItem]],
        minimum_support: float = 0.5,
        minimum_confidence: float = 0.8,
    ) -> None:
        self.minimum_support = minimum_support
        self.minimum_confidence = minimum_confidence

        k = 1
        self.candidate_itemsets: list[set[ItemCombo]] = []
        self.pruned_itemsets: list[set[ItemCombo]] = []
        self.frequency_history: list[dict[ItemCombo, int]] = []
        self.support_history: list[dict[ItemCombo, float]] = []
        self.frequent_itemsets: list[set[ItemCombo]] = [
            {frozenset({item}) for transaction in data for item in transaction}
        ]

        while self.frequent_itemsets[k - 1]:
            # Generate candidate
            candidates = self.get_candidate_combinations(
                items=self.frequent_itemsets[k - 1], size=k
            )
            self.candidate_itemsets.append(candidates)

            # Prune candidates
            if k > 1:
                candidates = self.prune_candidates(
                    candidates=candidates,
                    previous_candidates=self.frequent_itemsets[k - 1],
                    size=k - 1,
                )
            self.pruned_itemsets.append(candidates)

            # Calculate frequencies
            frequencies = self.get_frequency_per_candidate(
                transactions=data, candidates=candidates
            )
            self.frequency_history.append(frequencies)

            # Calculate support
            supports = self.get_support_per_candidate(
                transactions=data, candidate_frequencies=frequencies
            )
            self.support_history.append(supports)

            # Filter out candidates without minimum support
            candidates_with_minimum_support = {
                candidate
                for candidate, support in supports.items()
                if support >= self.minimum_support
            }
            self.frequent_itemsets.append(candidates_with_minimum_support)
            k += 1

        self.all_frequencies = self.get_all_frequencies()

    def get_candidate_combinations(
        self, items: set[ItemCombo], size: int
    ) -> set[ItemCombo]:
        individual_items = {separated_item for item in items for separated_item in item}
        combinations = itertools.combinations(individual_items, r=size)
        return {frozenset(combination) for combination in combinations}

    def get_frequency_per_candidate(
        self, transactions: Sequence[set[BrandItem]], candidates: set[ItemCombo]
    ) -> dict[ItemCombo, int]:
        candidate_frequencies: dict[ItemCombo, int] = defaultdict(int)

        for candidate in candidates:
            for transaction in transactions:
                if all(item in transaction for item in candidate):
                    candidate_frequencies[candidate] += 1

        return candidate_frequencies

    def get_support_per_candidate(
        self,
        transactions: Sequence[set[BrandItem]],
        candidate_frequencies: dict[ItemCombo, int],
    ) -> dict[ItemCombo, float]:
        candidate_support: dict[ItemCombo, float] = {}
        total_transactions = len(transactions)

        for candidate, frequency in candidate_frequencies.items():
            candidate_support[candidate] = frequency / total_transactions

        return candidate_support

    def prune_candidates(
        self, candidates: set[ItemCombo], previous_candidates: set[ItemCombo], size: int
    ) -> set[ItemCombo]:
        pruned_candidates = candidates.copy()

        for candidate in candidates:
            subsets = itertools.combinations(candidate, r=size)
            for subset in subsets:
                joined_subset = frozenset(subset)
                if joined_subset not in previous_candidates:
                    pruned_candidates.remove(candidate)
                    break

        return pruned_candidates

    def get_immediate_supersets(
        self, current_itemset: ItemCombo, next_itemsets: set[ItemCombo]
    ) -> Sequence[ItemCombo]:
        supersets: list[ItemCombo] = []

        for next_itemset in next_itemsets:
            if all(item in next_itemset for item in current_itemset):
                supersets.append(next_itemset)

        return supersets

    def get_maximal_frequent_itemsets(self) -> list[tuple[int, ItemCombo]]:
        # Maximal -> none of its immediate supersets is frequent
        maximal_itemsets: list[tuple[int, ItemCombo]] = []

        for k in range(1, len(self.frequent_itemsets) - 2):
            for frequent_itemset in self.frequent_itemsets[k]:
                supersets = self.get_immediate_supersets(
                    current_itemset=frequent_itemset,
                    next_itemsets=self.frequent_itemsets[k + 1],
                )

                # If no frequent superset, it is maximal
                if not supersets:
                    maximal_itemsets.append((k, frequent_itemset))

        return maximal_itemsets

    def get_closed_frequent_itemsets(self) -> list[tuple[int, ItemCombo]]:
        # Closed -> none of its immediate supersets has the same support as the itemset
        closed_itemsets: list[tuple[int, ItemCombo]] = []

        for k in range(1, len(self.frequent_itemsets) - 2):
            for frequent_itemset in self.frequent_itemsets[k]:
                current_support = self.support_history[k - 1][frequent_itemset]
                supersets = self.get_immediate_supersets(
                    current_itemset=frequent_itemset,
                    next_itemsets=self.frequent_itemsets[k + 1],
                )

                # If no frequent superset, or current support is not the
                # same as the support of any superset, it is closed
                if not supersets or all(
                    current_support != self.support_history[k][superset]
                    for superset in supersets
                ):
                    closed_itemsets.append((k, frequent_itemset))

        return closed_itemsets

    def generate_association_rules(self) -> list[tuple[str, float]]:
        association_rules: list[tuple[ItemCombo, ItemCombo, float]] = []

        for k in range(1, len(self.frequent_itemsets) - 2):
            for frequent_itemset in self.frequent_itemsets[k]:
                supersets = self.get_immediate_supersets(
                    current_itemset=frequent_itemset,
                    next_itemsets=self.frequent_itemsets[k + 1],
                )
                for superset in supersets:
                    for a, b in (
                        (frequent_itemset, superset),
                        (superset, frequent_itemset),
                    ):
                        confidence = self.all_frequencies[b] / self.all_frequencies[a]
                        if confidence >= self.minimum_confidence:
                            association_rules.append((a, b, confidence))

        sorted_rules = sorted(
            association_rules, key=lambda x: (len(x[0]), len(x[1]), x[2])
        )
        return [
            (
                f"{format_item_combo(a)} ——> {format_item_combo(b)}",
                confidence,
            )
            for a, b, confidence in sorted_rules
        ]

    def get_all_frequencies(self) -> dict[ItemCombo, int]:
        frequencies: dict[ItemCombo, int] = {}

        for frequency in self.frequency_history:
            frequencies |= frequency

        return frequencies

    @property
    def association_rules(self) -> str:
        rules = self.generate_association_rules()

        rules_string = format_table(
            headers=(f"Association Rule", "Confidence"),
            data=rules,
        )

        return rules_string

    @property
    def maximal_frequent_itemsets(self) -> str:
        maximal_itemsets = self.get_maximal_frequent_itemsets()

        maximal_string = label(f"Maximal frequent itemsets")
        for k, maximal_itemset in maximal_itemsets:
            maximal_string += f"\n[Level {k}] {format_item_combo(maximal_itemset)}"

        return maximal_string

    @property
    def closed_frequent_itemsets(self) -> str:
        closed_itemsets = self.get_closed_frequent_itemsets()

        closed_string = label(f"Closed frequent itemsets")
        for k, closed_itemset in closed_itemsets:
            closed_string += f"\n[Level {k}] {format_item_combo(closed_itemset)}"

        return closed_string

    def __str__(self) -> str:
        apriori_string = ""

        for i in range(len(self.candidate_itemsets) - 1):
            j = i + 1
            apriori_string += label(f"Level {j}")
            apriori_string += f"\n{j}-candidates: [{', '.join(format_item_combo(c) for c in self.candidate_itemsets[i])}]\n"

            apriori_string += format_table(
                headers=(f"Pruned {j}-candidates", "Support"),
                data=[
                    (item, self.support_history[i][item])
                    for item in self.pruned_itemsets[i]
                ],
            )
            apriori_string += format_table(
                headers=(f"Frequent {j}-itemsets", "Support"),
                data=[
                    (item, self.support_history[i][item])
                    for item in self.frequent_itemsets[j]
                ],
            )

        return apriori_string
