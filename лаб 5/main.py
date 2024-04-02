from rule import *
from formal_language import *

def print_rules(rules): 
    print("Правила для языка")
    for rule in rules:
        print(f"   {rule.get_key()} --> {rule.get_value()}")

if __name__ == "__main__":
    print("Задание 5")

    dict1 = [
        Rule("S", "aSL"),
        Rule("S", "aL"),
        Rule("L", "Kc"),
        Rule("cK", "Kc"),
        Rule("K", "b"),
    ]

    print_rules(dict1)
    fl = FormalLanguage(dict1)
    print("Цепочка: " + fl.translate("S"))
    print("Язык: L = {a^n b^m c^k | a, b, k > 0}")

    dict2 = [
        Rule("S", "aSBc"),
        Rule("S", "abc"),
        Rule("cB", "Bc"),
        Rule("bB", "bb"),
    ]

    print_rules(dict2)
    fl1 = FormalLanguage(dict2)
    print("Цепочка: " + fl1.translate("S"))
    print("Язык: L = {a^n b^m c^k | a, b, k > 0}")

    print("Грамматики эквиваленты, так как они определяют один и тот же язык")
    