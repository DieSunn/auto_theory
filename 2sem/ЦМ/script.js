// Матрица переходов: строки — текущее состояние, столбцы — следующее слово
const matrix = {
    "Ехал": {"Грека": 1},
    "Грека": {"видит": 1/5, "сунул": 1/5, "через": 1/5, "в": 2/5},
    "видит": {"реку": 1},
    "сунул": {"руку": 1},
    "через": {"реку": 1},
    "в": {"реке": 1/2, "руку": 1/2},
    "реку": {"Грека": 1/5, "сунул": 1/5, "видит": 1/5, "за": 1/5, "реку": 1/5},
    "руку": {"Греку": 1/3, "цап": 2/3},
    "Греку": {"руку": 1},
    "цап": {},
    "за": {"реку": 1},
    "реке": {"рак": 1},
    "рак": {"за": 1/2, "реку": 1/2}
};

// Функция для генерации случайного следующего состояния на основе вероятностей
function getNextWord(current) {
    const transitions = matrix[current];
    if (!transitions) return null;

    const rand = Math.random();
    let sum = 0;
    for (let [word, prob] of Object.entries(transitions)) {
        sum += prob;
        if (rand <= sum) return word;
    }
    return null;
}

// Генератор скороговорки
function generatePhrase() {
    let currentWord = "Ехал";
    let phrase = [currentWord];

    while (currentWord) {
        currentWord = getNextWord(currentWord);
        if (currentWord) phrase.push(currentWord);
    }

    document.getElementById("output").innerText = phrase.join(" ");
}

// Функция для отображения матрицы переходов в таблице
function displayMatrix() {
    const table = document.getElementById("transitionTable");
    let headerRow = "<tr><th></th>";

    // Генерация заголовков
    for (let state in matrix) {
        headerRow += `<th>${state}</th>`;
    }
    headerRow += "</tr>";
    table.innerHTML = headerRow;

    // Заполнение таблицы вероятностями
    for (let state in matrix) {
        let row = `<tr><th>${state}</th>`;
        for (let target in matrix) {
            let prob = matrix[state][target] || 0;
            // Округляем до 2 знаков после запятой
            row += `<td>${prob.toFixed(2)}</td>`;
        }
        row += "</tr>";
        table.innerHTML += row;
    }
}


// Отображение матрицы при загрузке страницы
window.onload = function() {
    displayMatrix();
};
