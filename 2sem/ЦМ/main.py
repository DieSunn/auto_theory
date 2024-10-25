import numpy as np
import tkinter as tk
from tkinter import scrolledtext, messagebox
from collections import defaultdict
import random

# Функция для создания матрицы переходов
def build_transition_matrix(text):
    # Убираем пунктуацию и разбиваем текст на слова
    words = text.replace('.', '').replace(':', '').replace('—', '').split()
    
    # Список уникальных слов
    unique_words = list(set(words))
    
    # Создаем индексное отображение слов
    word_to_idx = {word: idx for idx, word in enumerate(unique_words)}
    idx_to_word = {idx: word for word, idx in word_to_idx.items()}
    
    # Инициализация матрицы переходов
    transition_matrix = np.zeros((len(unique_words), len(unique_words)))

    # Заполнение матрицы
    for i in range(len(words) - 1):
        current_word = words[i]
        next_word = words[i + 1]
        transition_matrix[word_to_idx[current_word], word_to_idx[next_word]] += 1

    # Нормализация по строкам
    for i in range(len(transition_matrix)):
        row_sum = np.sum(transition_matrix[i])
        if row_sum > 0:
            transition_matrix[i] = transition_matrix[i] / row_sum
    
    return transition_matrix, word_to_idx, idx_to_word, words[0]  # Возвращаем первое слово текста

# Функция для вывода вероятностей переходов
def print_transition_probabilities(matrix, idx_to_word):
    result = ""
    for i, row in enumerate(matrix):
        result += f"Переходы для слова '{idx_to_word[i]}':\n"
        for j, prob in enumerate(row):
            if prob > 0:
                result += f"  -> {idx_to_word[j]}: {prob:.3f}\n"
        result += "\n"
    return result

# Функция для генерации текста по цепи Маркова
def generate_text_by_markov_chain(matrix, word_to_idx, idx_to_word, first_word, length=10):
    # Начинаем с первого слова скороговорки
    current_word_idx = word_to_idx[first_word]
    sentence = [first_word]

    for _ in range(length - 1):
        next_word_probs = matrix[current_word_idx]
        if np.sum(next_word_probs) == 0:  # Если нет доступных переходов
            current_word_idx = random.choice(list(word_to_idx.values()))
        else:
            # Выбираем следующее слово на основе вероятностей
            next_word_idx = np.random.choice(range(len(next_word_probs)), p=next_word_probs)
            sentence.append(idx_to_word[next_word_idx])
            current_word_idx = next_word_idx
    
    return ' '.join(sentence)

# Функция для вывода полной матрицы
def display_full_matrix(matrix, idx_to_word):
    matrix_str = "Полная матрица переходов:\n\n"
    matrix_str += "\t" + "\t".join([idx_to_word[i] for i in range(len(idx_to_word))]) + "\n"
    for i, row in enumerate(matrix):
        matrix_str += idx_to_word[i] + "\t" + "\t".join([f"{prob:.2f}" for prob in row]) + "\n"
    return matrix_str

# Функция, которая вызывается при нажатии кнопки для генерации матрицы переходов
def generate_matrix():
    input_text = text_input.get("1.0", tk.END).strip()  # Получение текста из текстового поля
    if not input_text:
        messagebox.showwarning("Ошибка", "Введите текст для анализа!")
        return
    
    global transition_matrix, word_to_idx, idx_to_word, first_word
    transition_matrix, word_to_idx, idx_to_word, first_word = build_transition_matrix(input_text)
    
    # Показ вероятностей переходов
    probabilities_result = print_transition_probabilities(transition_matrix, idx_to_word)
    transition_probabilities_display.delete(1.0, tk.END)
    transition_probabilities_display.insert(tk.END, probabilities_result)
    
    # Показ полной матрицы переходов
    matrix_result = display_full_matrix(transition_matrix, idx_to_word)
    matrix_display.delete(1.0, tk.END)
    matrix_display.insert(tk.END, matrix_result)

# Функция для генерации текста на основе цепи Маркова
def generate_text():
    if transition_matrix is None or word_to_idx is None or idx_to_word is None:
        messagebox.showwarning("Ошибка", "Сначала сгенерируйте матрицу переходов.")
        return
    
    generated_sentence = generate_text_by_markov_chain(transition_matrix, word_to_idx, idx_to_word, first_word, length=15)
    
    generated_text_display.delete(1.0, tk.END)
    generated_text_display.insert(tk.END, generated_sentence)

# Создание главного окна
window = tk.Tk()
window.title("Цепь Маркова по скороговорке")

# Главная рамка
main_frame = tk.Frame(window)
main_frame.pack(padx=10, pady=10)

# Поле для ввода текста скороговорки
input_frame = tk.Frame(main_frame)
input_frame.pack(fill=tk.BOTH, expand=True)

tk.Label(input_frame, text="Введите текст скороговорки:").pack(anchor='w', pady=5)
text_input = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, width=60, height=5)
text_input.pack(fill=tk.BOTH, pady=5)

# Кнопка для генерации матрицы переходов
generate_button = tk.Button(main_frame, text="Сгенерировать матрицу переходов", command=generate_matrix)
generate_button.pack(pady=5)

# Раздел с результатами: матрица переходов, вероятности и сгенерированный текст
results_frame = tk.Frame(main_frame)
results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

# Поле для вывода вероятностей переходов
tk.Label(results_frame, text="Вероятности переходов:").pack(anchor='w')
transition_probabilities_display = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, width=60, height=10)
transition_probabilities_display.pack(fill=tk.BOTH, pady=5)

# Поле для вывода полной матрицы
tk.Label(results_frame, text="Полная матрица переходов:").pack(anchor='w')
matrix_display = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, width=60, height=10)
matrix_display.pack(fill=tk.BOTH, pady=5)

# Кнопка для генерации текста на основе цепи Маркова
generate_text_button = tk.Button(main_frame, text="Сгенерировать текст", command=generate_text)
generate_text_button.pack(pady=5)

# Поле для вывода сгенерированного текста
tk.Label(main_frame, text="Сгенерированный текст:").pack(anchor='w')
generated_text_display = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=60, height=5)
generated_text_display.pack(fill=tk.BOTH, pady=5)

# Переменные для хранения матрицы и индексов слов
transition_matrix = None
word_to_idx = None
idx_to_word = None
first_word = None

# Запуск основного цикла приложения
window.mainloop()
