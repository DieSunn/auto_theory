import random

class FormalLanguage:
    def __init__(self, rules, max_repetitions_count=10000):
        """
        Инициализация объекта формального языка.

        Параметры:
        - rules: список правил языка
        - max_repetitions_count: максимальное количество повторений при выводе
        """
        self.rules = rules  # Правила языка
        self.max_repetitions_count = max_repetitions_count  # Максимальное количество повторений

    def set_rules(self, rules):
        """
        Метод для установки правил языка.

        Параметры:
        - rules: список правил языка
        """
        self.rules = rules

    def get_rules(self):
        """
        Метод для получения правил языка.
        """
        return self.rules

    def set_max_repetitions_count(self, max_repetitions_count):
        """
        Метод для установки максимального количества повторений при выводе.

        Параметры:
        - max_repetitions_count: максимальное количество повторений
        """
        self.max_repetitions_count = max_repetitions_count

    def get_max_repetitions_count(self):
        """
        Метод для получения максимального количества повторений при выводе.
        """
        return self.max_repetitions_count

    def output_left(self):
        """
        Метод для выполнения левостороннего вывода строки на основе правил языка.
        """
        result = "S"  # Начальная цепочка
        count = 0  # Счетчик повторений
        while count < self.max_repetitions_count:
            pos = -1  # Индекс крайнего левого нетерминального символа

            # Поиск крайнего левого нетерминального символа в цепочке
            for rule in self.rules:
                key = rule.get_key()
                find_pos = result.find(key)
                if (pos > find_pos or pos == -1) and find_pos != -1:
                    pos = find_pos

            if pos == -1:
                break

            rules = []  # Список правил для крайнего левого нетерминального символа
            for rule in self.rules:
                key = rule.get_key()
                if pos == result.find(key):
                    rules.append(rule)

            index = random.randint(0, len(rules) - 1)  # Случайный выбор правила
            r = rules[index]

            p = result.find(r.get_key())  # Позиция крайнего левого нетерминального символа
            # Замена крайнего левого нетерминального символа на его правую часть
            result = result[:p] + r.get_value() + result[p + len(r.get_key()):]

            count += 1  # Увеличение счетчика повторений

        return result

    def translate(self, text):
        """
        Метод для перевода строки на формальный язык.

        Параметры:
        - text: строка для перевода
        """
        count = 0  # Счетчик повторений
        is_end = False  # Флаг, указывающий на завершение перевода
        while count < self.max_repetitions_count:
            if is_end:
                break

            count += 1  # Увеличение счетчика повторений
            is_end = True

            for rule in self.rules:
                if not rule.get_is_looped():
                    key = rule.get_key()
                    value = rule.get_value()
                    pos = text.find(key)

                    if pos != -1:
                        # Проверка на зацикливание и применение правила к строке
                        if self.check_loop(text, rule):
                            rule.set_is_looped(True)
                        else:
                            text = text[:pos] + value + text[pos + len(key):]
                            is_end = False
                            break
                else:
                    rule.set_is_looped(not rule.get_is_looped())

        self.refresh_rules()  # Обновление флагов зацикливания правил
        return text

    def check_loop(self, input_str, rule, count=5):
        """
        Метод для проверки правила на зацикливание.

        Параметры:
        - input_str: строка, к которой применяется правило
        - rule: правило языка
        - count: количество допустимых повторений
        """
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
        """
        Метод для обновления флагов зацикливания правил.
        """
        for rule in self.rules:
            rule.set_is_looped(False)