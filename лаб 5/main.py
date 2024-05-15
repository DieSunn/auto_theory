import random

class Rule:
    def __init__(self, a, b, l=False):
        self.A = a
        self.B = b
        self.isLooped = l

def print_rules(rules):
    print("Правила для языка:")
    for rule in rules:
        print(rule.A, "->", rule.B)

class FormalLanguage:
    def __init__(self, rules, count=100):
        self.rules = rules
        self.MaxRepetitionsCount = count

    def check_loop(self, input_str, rule, count=10):
        for _ in range(count):
            A = rule.A
            B = rule.B
            pos = input_str.find(A)
            if pos != -1:
                input_str = input_str[:pos] + B + input_str[pos + len(A):]
            else:
                return False
        return True

    def refresh_rules(self):
        for rule in self.rules:
            rule.isLooped = False

    def translate(self, text):
        count = 0
        is_end = False
        while count < self.MaxRepetitionsCount:
            if is_end:
                break
            count += 1
            is_end = True
            for rule in self.rules:
                if not rule.isLooped:
                    A = rule.A
                    B = rule.B
                    pos = text.find(A)
                    if pos != -1:
                        if self.check_loop(text, rule):
                            rule.isLooped = True
                        else:
                            text = text[:pos] + B + text[pos + len(A):]
                            is_end = False
                            break
                else:
                    rule.isLooped = True
        self.refresh_rules()
        return text

    def output_left(self):
        result = "S"
        count = 0
        while count < self.MaxRepetitionsCount:
            pos = float('inf')
            for rule in self.rules:
                key = rule.A
                find_pos = result.find(key)
                if (pos > find_pos or pos == float('inf')) and find_pos != -1:
                    pos = find_pos
            if pos == float('inf'):
                break
            rules_ = [rule for rule in self.rules if pos == result.find(rule.A)]
            index = random.randint(0, len(rules_) - 1)
            r = rules_[index]
            p = result.find(r.A)
            result = result[:p] + r.B + result[p + len(r.A):]
            count += 1
        return result

    def output_left_equivalence(self):
        result = "S"
        count = 0
        while count < self.MaxRepetitionsCount:
            pos = float('inf')
            for rule in self.rules:
                key = rule.A
                find_pos = result.find(key)
                if (pos > find_pos or pos == float('inf')) and find_pos != -1:
                    pos = find_pos
            if pos == float('inf'):
                break
            rules_ = [rule for rule in self.rules if pos == result.find(rule.A)]
            index = random.randint(0, len(rules_) - 1)
            r = rules_[index]
            p = result.find(r.A)
            result = result[:p] + r.B + result[p + len(r.A):]
            count += 1
        return result

    def transformations(self, chain_):
        buf = ""
        result = ""
        transformations = []
        found = False
        counter = 0
        while not found:
            buf = self.output_left()
            counter += 1
            if counter == 10000000:
                return "Цепочка не построена. Попробуйте ещё раз\n"
            if buf == chain_:
                found = True
        for transformation in transformations:
            result += transformation + "\n"
        result = "Начальный символ: S\n" + result
        return result

def fill_vector_with_unique_chars(input_string, vector):
    for c in input_string:
        if c not in vector:
            vector.append(c)

def equivalence(fl1, fl2):
    alphabet1, alphabet2 = [], []
    buf1, buf2 = "", ""
    transformations = []
    for _ in range(10000):
        buf1 = fl1.output_left_equivalence()
        buf2 = fl2.output_left_equivalence()
        fill_vector_with_unique_chars(buf1, alphabet1)
        fill_vector_with_unique_chars(buf2, alphabet2)
    alphabet1.sort()
    alphabet2.sort()
    print("\nСимволы в первом языке:", alphabet1)
    print("Символы во втором языке:", alphabet2)
    if alphabet1 == alphabet2:
        return "Грамматики эквивалентны"
    else:
        return "Грамматики не эквивалентны"

class Grammar:
    def __init__(self, vn, vt, rules, s="S"):
        self.Nonterminal = vn
        self.Terminal = vt
        self.P = rules
        self.S = s

    def get_type_grammar(self):
        is_type_one = True
        is_type_two = True
        is_type_three = True

        is_each_term_pos_bigger = True
        is_each_term_pos_smaller = True

        for r in self.P:
            is_type_one &= len(r.A) <= len(r.B)

            for vt in self.Terminal:
                is_type_two &= vt not in r.A

            if is_each_term_pos_bigger or is_each_term_pos_smaller:
                terminal_positions = []
                non_terminal_positions = []
                for vn in self.Nonterminal:
                    temp = r.B.find(vn)
                    if temp != -1:
                        non_terminal_positions.append(temp)
                for vt in self.Terminal:
                    temp = r.B.find(vt)
                    if temp != -1:
                        terminal_positions.append(temp)
                for pos in terminal_positions:
                    for pos_non_term in non_terminal_positions:
                        is_each_term_pos_bigger &= pos > pos_non_term
                        is_each_term_pos_smaller &= pos < pos_non_term
                if not is_each_term_pos_bigger and not is_each_term_pos_smaller:
                    is_type_three = False

        res = "0"
        if is_type_one:
            res += " 1"
        if is_type_two:
            res += " 2"
        if is_type_three:
            res += " 3"
        return res

    def make_tree(self, text):
        max_count = 10000
        count = 0
        tree = [text]

        while count < max_count:
            for rule in self.P:
                key = rule.A
                value = rule.B

                pos = text.find(value)
                if pos != -1:
                    text = text[:pos] + key + text[pos + len(value):]

                    separator = "|"
                    for i in range(pos):
                        separator = " " + separator
                    tree.append(separator)
                    tree.append(text)
            count += 1

        for item in reversed(tree):
            print(item)
        return text



def enum_to_string(s):
    state_to_string = {
        'H': "H",
        'N': "N",
        'P': "P",
        'S': "S",
        'ER': "ER"
    }
    return state_to_string[s]

def enum_to_string_2(s):
    state_to_string = {
        'H_': "H",
        'A_': "A",
        'B_': "B",
        'S_': "S",
        'ER_': "ER"
    }
    return state_to_string[s]

def enum_to_string_3(s):
    state_to_string = {
        'H_': "H",
        'A_': "A",
        'B_': "B",
        'S_': "S",
        'ER_': "ER"
    }
    return state_to_string[s]




# Задание 9
print("\nЗадание 9\n")
dict3 = [
    Rule("S", "aSbS"),
    Rule("S", "bSaS"),
    Rule("S", "E")
]
print_rules(dict3)
fl14 = FormalLanguage(dict3)
print("Цепочка:", fl14.translate("S"))

gr = Grammar(["S"], ["a", "b", "E"], dict3)
print(gr.make_tree("aEbaEbE"))

