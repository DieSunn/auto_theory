import random

class FormalLanguage:
    def __init__(self, rules, count=10000):
        self._rules = rules
        self.MaxRepetitionsCount = count

    def set_rules(self, rules):
        self._rules = rules

    def get_rules(self):
        return self._rules

    def set_max_repetitions_count(self, repeat):
        self.MaxRepetitionsCount = repeat

    def get_max_repetitions_count(self):
        return self.MaxRepetitionsCount

    def check_loop(self, input_str, rule, count=5):
        for i in range(count):
            key = rule.get_key()
            value = rule.get_value()

            pos = input_str.find(key)

            if pos != -1:
                input_str = input_str[:pos] + value + input_str[pos + len(key):]
            else:
                return False
        return True

    def refresh_rules(self):
        for rule in self._rules:
            rule.set_is_looped(False)

    def output_left(self, transformations=None):
        if transformations is None:
            transformations = []
        result = "S"
        count = 0
        while count < self.MaxRepetitionsCount:
            pos = -1
            for rule in self._rules:
                key = rule.get_key()
                find_pos = result.find(key)
                if (pos > find_pos or pos == -1) and find_pos != -1:
                    pos = find_pos
                    break

            if pos == -1:
                break

            rules = [rule for rule in self._rules if result.find(rule.get_key()) == pos]

            index = random.randint(0, len(rules) - 1)
            r = rules[index]

            p = result.find(r.get_key())
            result = result[:p] + r.get_value() + result[p + len(r.get_key()):]
            transformations.append(result)
            count += 1

        return result

    def transformations(self, chain_):
        transformations = []
        buf = ''
        result = ''
        found = False
        counter = 0
        while not found:
            buf = self.output_left(transformations)
            counter += 1
            if counter == 10000000:
                return "Цепочка не построена. Попробуйте ещё раз\n"
            if buf == chain_:
                found = True

        for transformation in transformations:
            result += transformation + "\n"
        result = "Начальный символ: S\n" + result

        return result

    def translate(self, text):
        count = 0
        is_end = False
        while count < self.MaxRepetitionsCount:
            if is_end:
                break

            count += 1
            is_end = True
            for rule in self._rules:
                if not rule.get_is_looped():
                    key = rule.get_key()
                    value = rule.get_value()

                    pos = text.find(key)

                    if pos != -1:
                        if self.check_loop(text, rule):
                            rule.set_is_looped(True)
                        else:
                            text = text[:pos] + value + text[pos + len(key):]
                            is_end = False
                            break
                else:
                    rule.set_is_looped(not rule.get_is_looped())

        self.refresh_rules()
        return text