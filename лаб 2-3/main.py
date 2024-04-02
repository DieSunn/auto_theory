from rule import Rule
from formal_language import FormalLanguage

def print_rules(rules):
    print("Правила для языка")
    for rule in rules:
        print(f"   {rule.get_key()} --> {rule.get_value()}")

if __name__ == "__main__":
    print("Первая лабораторная работа.")
    print("Задание 2.a")

    dict1 = [
        Rule("S", "aaCFD"),
        Rule("AD", "D"),
        Rule("F", "AFB"),
        Rule("F", "AB"),
        Rule("Cb", "bC"),
        Rule("AB", "bBA"),
        Rule("CB", "C"),
        Rule("Ab", "bA"),
        Rule("bCD", "\u03B5")  # epsilon ε
    ]

    print_rules(dict1)
    fl1 = FormalLanguage(dict1)
    print("Цепочка", fl1.translate("S"))
    print("Язык: L = { a^n | n > 0 }")

    print("\nЗадание 2.б")

    dict2 = [
        Rule("S", "A|"),
        Rule("S", "B|"),
        Rule("A", "a"),
        Rule("A", "Ba"),
        Rule("b", "b"),
        Rule("b", "Bb"),
        Rule("b", "Ab")
    ]

    print_rules(dict2)
    fl2 = FormalLanguage(dict2)
    print("Цепочка", fl2.translate("S"))
    print("Язык: L = { (a|)^n | n>0 }")
    
    print("\nЗадание 3.a")
    print("Язык: L = { a^n b^m c^k | n, m, k > 0}")
    print("Грамматика: G: ({a, b, c}, {A, B, C}, P, S)")
    dict_1 = [
        Rule("S", "aaB"),
        Rule("B", "bCCCC"),
        Rule("B", "b"),
        Rule("C", "Cc"),
        Rule("C", "c"),
    ]
    print_rules(dict_1)
    fl3 = FormalLanguage(dict_1)
    print("Цепочка: " + fl3.translate("S"))

    print("\nЗадание 3.б")
    print("Язык: L = {0^n(10)^m | n, m ≥ 0}")
    print("Грамматика: G: ({0, 10}, {A, B}, P, S)")
    dict_2 = [
        Rule("S", "0AB"),
        Rule("A", "000"),
        Rule("B", "1010"),
    ]
    print_rules(dict_2)
    fl4 = FormalLanguage(dict_2)
    print("Цепочка: " + fl4.translate("S"))

    print("\nЗадание 3.в")
    print("Язык: L = {a1 a2 … an an … a2a1 | ai E {0, 1}}")
    print("Грамматика: G: ({0, 1}, {A, B}, P, S)")
    dict_3 = [
        Rule("S", "AB"),
        Rule("A", "1001010"),
        Rule("B", "0101001"),
    ]
    print_rules(dict_3)
    fl5 = FormalLanguage(dict_3)
    print("Цепочка: " + fl5.translate("S"))