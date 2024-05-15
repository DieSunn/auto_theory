// Модифицированный конструктор машины Тьюринга с дополнительным состоянием для переноса
class TuringMachine {
  constructor() {
    this.tape = []; // Входная лента
    this.head = 0; // Позиция головки
    this.state = "q0"; // Начальное состояние
    this.isRunning = false; // Флаг для определения выполнения
    this.steps = []; // Массив для хранения шагов выполнения
    this.carry = false; // Флаг для переноса
  }

  step() {
    if (!this.isRunning) return;

    const symbol = this.tape[this.head];

    const stepInfo = {
      tapeSnapshot: [...this.tape],
      headPosition: this.head,
      state: this.state,
    };
    this.steps.push(stepInfo);

    switch (this.state) {
      case "q0":
        if (symbol === "1") {
          this.tape[this.head] = "1";
          this.moveHeadRight();
          this.state = "q1";
        } else if (symbol === "+") {
          this.tape[this.head] = " ";
          this.moveHeadRight();
          this.state = "q_add";
        } else {
          this.halt();
        }
        break;
      case "q1":
        if (symbol === "1") {
          this.moveHeadRight();
        } else {
          this.tape[this.head] = "1";
          this.state = "q_accept";
        }
        break;
      case "q_add":
        if (symbol === "1") {
          this.moveHeadRight();
          if (this.head === this.tape.length) {
            this.tape.push(" ");
          }
        } else {
          if (this.carry) {
            this.moveHeadLeft();
            if (this.head === -1) {
              this.tape.unshift(" ");
              this.head = 0;
            }
            this.tape[this.head] = "1";
            this.carry = false;
          } else {
            // Проверяем, если последний символ перед головкой - это "1", удаляем его
            if (this.tape[this.head - 1] === "1") {
              this.tape.pop();
            }
            this.tape[this.head] = "1";
          }
          this.state = "q1";
        }
        break;
      case "q_accept":
        this.isRunning = false;
        if (this.tape[this.tape.length - 1] === "1") {
            this.tape.pop(); // Удаляем последнюю лишнюю единицу
        }

        break;
    }

    if (this.state === "q_accept" || this.state === "q_reject") {
      this.isRunning = false;
    }
}


  // Метод для перемещения головки вправо
  moveHeadRight() {
    this.head++;
    // Если достигнут конец ленты, добавляем новую ячейку
    if (this.head === this.tape.length) {
      this.tape.push(" ");
    }
  }

  // Метод для остановки выполнения машины Тьюринга
  halt() {
    this.isRunning = false; // Останавливаем выполнение
    this.state = "q_reject"; // Переходим в состояние отклонения
    console.log("Машина Тьюринга завершила работу с ошибкой.");
  }

  // Метод для выполнения машины Тьюринга пошагово
  stepRun() {
    this.step(); // Выполняем один шаг
  }

  // Метод для запуска машины Тьюринга
  run() {
    this.isRunning = true; // Устанавливаем флаг выполнения
    while (
      this.isRunning &&
      this.state !== "q_accept" &&
      this.state !== "q_reject"
    ) {
      this.step(); // Выполняем шаги машины Тьюринга, пока выполнение не остановлено или не достигнут конец
    }
  }

  // Метод для получения массива с шагами выполнения
  getSteps() {
    return this.steps;
  }

  // Метод для сброса состояния машины Тьюринга
  reset() {
    this.tape = []; // Сбрасываем состояние ленты
    this.head = 0; // Сбрасываем позицию головки
    this.state = "q0"; // Сбрасываем состояние
    this.isRunning = false; // Сбрасываем флаг выполнения
    this.steps = []; // Очищаем массив с шагами выполнения
  }
}

// Создаем экземпляр машины Тьюринга
const turingMachine = new TuringMachine();
// Функция для выполнения одного шага машины Тьюринга
function stepTuringMachine() {
  if (turingMachine.isRunning) {
    updateInterface(); // Обновляем интерфейс перед выполнением шага

    const stepsBefore = turingMachine.getSteps().length; // Сохраняем количество шагов до выполнения текущего шага
    turingMachine.stepRun(); // Выполняем один шаг
    const stepsAfter = turingMachine.getSteps().length; // Получаем количество шагов после выполнения текущего шага

    // Если добавился новый шаг (т.е. шаг был успешно выполнен), обновляем интерфейс
    if (stepsAfter > stepsBefore) {
      updateInterface(); // Обновляем интерфейс после каждого шага
    }
  }
}

// Модифицированная функция для установки конфигурации ленты
function setTape() {
  const inputTapeElement = document.getElementById("input-tape");
  const inputTapeValue = inputTapeElement.value;
  turingMachine.reset();

  console.log(inputTapeValue.split(""));
  if (/^1+\+1+$/.test(inputTapeValue)) {
    turingMachine.tape = inputTapeValue.split(""); // Используем введенное пользователем значение
    console.log(turingMachine.tape);
    updateInterface();
  } else {
    alert(
      "Please enter a valid unary tape configuration for addition (e.g., 11+11)"
    );
  }
}

// Функция для запуска машины Тьюринга
function runTuringMachine() {
  turingMachine.isRunning = true; // Устанавливаем флаг выполнения
}

// Функция для сброса состояния машины Тьюринга
function resetTuringMachine() {
  turingMachine.reset();
  updateInterface(); // Обновляем интерфейс после сброса
}

// Функция для обновления интерфейса
function updateInterface() {
  const tapeElement = document.getElementById("tape");
  const stepInfoElement = document.getElementById("step-info");

  // Очищаем предыдущее содержимое ленты
  tapeElement.innerHTML = "";

  // Получаем текущее состояние ленты и позицию головки
  const tape = turingMachine.tape;
  const headPosition = turingMachine.head;

  // Создаем и стилизуем ячейки ленты для каждого символа
  for (let i = 0; i < tape.length; i++) {
    const tapeCell = document.createElement("div");
    tapeCell.textContent = tape[i];
    tapeCell.classList.add("tape-cell");

    // Если текущая позиция головки равна индексу ячейки, добавляем стиль для выделения головки
    if (i === headPosition) {
      tapeCell.classList.add("head-position");
    }

    tapeElement.appendChild(tapeCell); // Добавляем ячейку на ленту
  }

  // Получаем текущий шаг выполнения
  const steps = turingMachine.getSteps();
  const currentStep = steps.length;

  // Если есть информация о шаге, обновляем отображение
  if (currentStep > 0) {
    const step = steps[currentStep - 1];
    const tapeSnapshot = step.tapeSnapshot.join(" ");
    const state = step.state;

    stepInfoElement.textContent = `Step ${currentStep}: Tape: ${tapeSnapshot}, Head: ${headPosition}, State: ${state}`;
  } else {
    stepInfoElement.textContent = ""; // Очищаем информацию о шаге, если шагов нет
  }

  // Если достигнуто конечное состояние и последняя ячейка лишняя, удаляем её
  if (turingMachine.state === "q_accept" && tape[tape.length - 1] === "1") {
    tapeElement.lastChild.remove();
  }
}
