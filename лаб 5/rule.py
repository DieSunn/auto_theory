import sys

class Rule:
    def __init__(self, k, v, l=False):
        self.key = k
        self.value = v
        self.is_looped = l

    def set_key(self, k):
        self.key = k

    def get_key(self):
        return self.key

    def set_value(self, v):
        self.value = v

    def get_value(self):
        return self.value

    def set_is_looped(self, l):
        self.is_looped = l

    def get_is_looped(self):
        return self.is_looped

def print_rules(rules):
    print("Правила для языка")
    for rule in rules:
        print(f"   {rule.get_key()} --> {rule.get_value()}")
