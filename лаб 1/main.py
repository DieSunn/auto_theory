from Rule import *
from FormalLanguage import *

def print_rules(rules):
    print("Правила для языка")
    for rule in rules:
        print(f"   {rule.get_key()} --> {rule.get_value()}")

if __name__ == "__main__":
    # dict1 = [
    #     Rule("S", "T"),
    #     Rule("S", "T+S"),
    #     Rule("S", "T-S"),
    #     Rule("T", "F"),
    #     Rule("T", "F*T"),
    #     Rule("F", "a"),
    #     Rule("F", "b"),
    # ]

    # print("Задание 1.a")
    # print_rules(dict1)
    # fl1 = FormalLanguage(dict1)
    # way1 = fl1.transformations("a-b*a+b")
    # print(way1)

    dict2 = [
        Rule("S", "aSBC"),
        Rule("S", "abC"),
        Rule("CB", "BC"),
        Rule("bB", "bb"),
        Rule("bC", "bc"),
        Rule("cC", "cc"),
    ]

    print("Задание 1.б")
    print_rules(dict2)
    fl2 = FormalLanguage(dict2)
    way2 = fl2.transformations("aaabbbccc")
    print(way2)