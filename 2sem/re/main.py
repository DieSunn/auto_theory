class SpellChecker:
    def __init__(self, dictionary_path):
        with open(dictionary_path, "r", encoding="utf-8") as file:
            self.dictionary = set(word.strip().lower() for word in file)
        self.dfa = DFA()

    def is_word_valid(self, word):
        """Проверяет слово с помощью DFA и словаря"""
        if not self.dfa.is_valid_word(word):  # Проверка структуры слова
            return False
        return word.lower() in self.dictionary  # Проверка наличия в словаре

    def calculate_levenshtein(self, word1, word2):
        len1, len2 = len(word1), len(word2)
        dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        for i in range(len1 + 1):
            for j in range(len2 + 1):
                if i == 0:
                    dp[i][j] = j
                elif j == 0:
                    dp[i][j] = i
                elif word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
        return dp[len1][len2]

    def suggest_corrections(self, word, max_suggestions=5, max_distance=3):
        """Предлагает исправления с фильтрацией по расстоянию и длине"""
        distances = {
            dict_word: self.calculate_levenshtein(word.lower(), dict_word)
            for dict_word in self.dictionary
            if abs(len(word) - len(dict_word)) <= max_distance  # Фильтр по длине
        }

        # Оставляем только слова с расстоянием <= max_distance
        filtered_suggestions = {
            word: dist for word, dist in distances.items() if dist <= max_distance
        }

        # Сортируем и возвращаем топ-N
        sorted_suggestions = sorted(
            filtered_suggestions.items(), key=lambda x: x[1]
        )
        return [word for word, dist in sorted_suggestions[:max_suggestions]]

    def check_text(self, text):
        """Проверка текста с улучшенными предложениями"""
        words = text.split()
        errors = {}

        for word in words:
            if not self.is_word_valid(word):  # Проверяем только некорректные слова
                suggestions = self.suggest_corrections(word)
                errors[word] = suggestions

        return errors



# DFA для проверки структуры слов
class DFA:
    def __init__(self):
        self.states = {
            "q0": {"alpha": "q1"},
            "q1": {"alpha": "q1", "end": "accept"},
        }
        self.current_state = "q0"
        self.accept_state = "accept"
    
    def reset(self):
        self.current_state = "q0"

    def transition(self, char):
        if char.isalpha():
            char_class = "alpha"
        else:
            char_class = "end"

        if char_class in self.states[self.current_state]:
            self.current_state = self.states[self.current_state][char_class]
        else:
            self.current_state = None  # Некорректный символ
    
    def is_valid_word(self, word):
        self.reset()
        for char in word:
            self.transition(char)
            if self.current_state is None:
                return False
        self.transition("end")
        return self.current_state == self.accept_state


# Пример использования
if __name__ == "__main__":
    # dictionary_path = "dictionary.txt"
    # checker = SpellChecker(dictionary_path)
    
    # input_text = "apple Bananna dog elphant wrongword"
    # errors = checker.check_text(input_text)
    
    dfa = DFA()
    test_words = ["apple", "Bananna", "dog", "123wrong", "elphant"]
    for word in test_words:
        print(f"'{word}': {dfa.is_valid_word(word)}")


    # if errors:
    #     print("Ошибки и варианты исправления:")
    #     for word, suggestions in errors.items():
    #         print(f"- {word}: {', '.join(suggestions) if suggestions else 'Нет предложений'}")
    # else:
    #     print("Ошибок не найдено!")
