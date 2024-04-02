class Rule:
    def __init__(self, key, value, is_looped=False):
        # Инициализация объекта правила языка.
        self.key = key  # Ключ (левая часть) правила.
        self.value = value  # Значение (правая часть) правила.
        self.is_looped = is_looped  # Флаг, указывающий, зацикливает ли правило грамматику.

    def set_key(self, key):
        # Метод для установки ключа правила.
        self.key = key

    def get_key(self):
        # Метод для получения ключа правила.
        return self.key

    def set_value(self, value):
        # Метод для установки значения правила.
        self.value = value

    def get_value(self):
        # Метод для получения значения правила.
        return self.value

    def set_is_looped(self, is_looped):
        # Метод для установки флага зацикливания правила.
        self.is_looped = is_looped

    def get_is_looped(self):
        # Метод для получения значения флага зацикливания правила.
        return self.is_looped


def print_rules(rules):
    # Функция для вывода правил языка.
    print("Правила для языка")
    for rule in rules:
        print(f"   {rule.get_key()} --> {rule.get_value()}")  # Вывод каждого правила в формате "ключ --> значение".
