from apriori import Apriori
from data import q1_database, q2_database
from formatting import title
from frequent_pattern_tree import FrequentPatternTree, get_sorted_item_frequencies


def question_1() -> None:
    print(title("Question 1"))
    transactions = tuple(q1_database.values())

    forward_tree = FrequentPatternTree(transactions)
    reverse_tree = FrequentPatternTree(transactions, reverse=True)
    sorted_frequencies = get_sorted_item_frequencies(transactions)

    print("\na) FP-Tree with lexicographic order.\n")
    print(forward_tree)
    print("b) FP-Tree with reverse lexicographic order.\n")
    print(reverse_tree)
    print("c) Ordered item frequencies.\n")
    print(sorted_frequencies)


def question_2() -> None:
    print(title("Question 2"))
    transactions = tuple(q2_database.values())

    apriori = Apriori(transactions)

    print("\na) Frequent itemsets per level are shown below in tables.")
    print(apriori)
    print("\nb) Below are the maximal and closed frequent itemsets, per level.")
    print(apriori.maximal_frequent_itemsets)
    print(apriori.closed_frequent_itemsets)
    print("\nc) Association rules of all frequent itemsets meeting confidence level.")
    print(apriori.association_rules)


if __name__ == "__main__":
    input("\nPress [Enter] for Question 1: ")
    question_1()
    input("\nPress [Enter] for Question 2: ")
    question_2()
