from FormalLanguage import FormalLanguage
from Rule import Rule

def print_rules(rules):
    print("Правила для языка")
    for rule in rules:
        print(f"   {rule.get_key()} --> {rule.get_value()}")

if __name__ == "__main__":
    print("Задание 6")

    dict1 = [
        Rule("S", "AB"),
        Rule("S", "ABS"),
        Rule("AB", "BA"),
        Rule("BA", "AB"),
        Rule("A", "a"),
        Rule("B", "b"),
    ]

    print_rules(dict1)
    fl = FormalLanguage(dict1)
    print("Цепочка: " + fl.translate("S"))

    dict2 = [
        Rule("S", "ab"),
    ]

    print_rules(dict2)
    fl1 = FormalLanguage(dict2)
    print("Цепочка: " + fl1.translate("S"))