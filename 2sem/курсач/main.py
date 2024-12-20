from flask import Flask, request, jsonify
from flask_cors import CORS
from bisect import bisect_left
from spellchecker import SpellChecker

app = Flask(__name__)
CORS(app)  # Включаем CORS для работы с фронтендом

# Инициализация орфографического словаря
spell = SpellChecker(language="ru")
filepath = "sorted_words.txt"  # Файл для пользовательского словаря


# Функции из первого кода
class LevenshteinAutomaton:
    def __init__(self, word, max_distance):
        self.word = word
        self.max_distance = max_distance

    def build_automaton(self):
        word_len = len(self.word)
        states = {}

        for i in range(word_len + 1):
            for j in range(self.max_distance + 1):
                states[(i, j)] = set()

        for i in range(word_len + 1):
            for j in range(self.max_distance + 1):
                if j < self.max_distance:
                    states[(i, j)].add((i, j + 1))  # Добавление символа
                if i < word_len:
                    states[(i, j)].add((i + 1, j + 1))  # Удаление символа
                    if j < self.max_distance:
                        states[(i, j)].add((i + 1, j + 1))  # Замена символа
                    states[(i, j)].add((i + 1, j))  # Совпадение символа

        self.states = states

    def match(self, input_word):
        current_states = {(0, 0)}

        for char in input_word:
            next_states = set()
            for state in current_states:
                i, j = state

                if j < self.max_distance:
                    next_states.add((i, j + 1))
                if i < len(self.word):
                    next_states.add((i + 1, j + 1))
                    if self.word[i] == char:
                        next_states.add((i + 1, j))
                    else:
                        next_states.add((i + 1, j + 1))

            current_states = next_states

        return any(state[0] == len(self.word) and state[1] <= self.max_distance for state in current_states)


def load_dictionary(filepath):
    try:
        with open(filepath, "r", encoding="windows-1251") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print("Файл словаря не найден. Создайте файл sorted_words.txt.")
        return []


def suggest_word(input_word, dictionary, max_distance):
    suggestions = []
    start_index = bisect_left(dictionary, input_word[:1])

    for word in dictionary[start_index:]:
        if not word.startswith(input_word[:1]):
            break

        lev_automaton = LevenshteinAutomaton(word, max_distance)
        lev_automaton.build_automaton()
        if lev_automaton.match(input_word):
            suggestions.append(word)

        if len(suggestions) >= 5:  # Ограничиваем количество предложений
            break

    return suggestions


# Flask-обработчик
@app.route('/receive-words', methods=['POST'])
def receive_words():
    data = request.get_json()
    if not data or 'words' not in data:
        return jsonify({"status": "error", "message": "Invalid data"}), 400

    words = data['words']  # Получаем словарь слов от клиента
    dictionary = load_dictionary(filepath)  # Загружаем словарь
    max_distance = 1  # Максимальное расстояние Левенштейна

    suggestions = {}
    for word_id, word in words.items():
        if word not in spell:  # Если слово некорректное
            suggested_words = suggest_word(word, dictionary, max_distance)
            if suggested_words:
                suggestions[word_id] = suggested_words

    if suggestions:
        response = {
            "status": "error",
            "message": "Words processed",
            "suggestions": suggestions,
        }
    else:
        response = {
            "status": "correct",
            "message": "Words processed",
            "suggestions": suggestions,
        }        
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
