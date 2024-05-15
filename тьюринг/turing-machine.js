<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Turing Machine Simulator</title>
    <style>
      /* CSS стили */
      .cell {
        border: 1px solid black;
        width: 30px;
        height: 30px;
        display: inline-block;
        text-align: center;
        line-height: 30px;
      }
      .highlight {
        background-color: lightblue;
      }
      .head {
        background-color: red;
      }
    </style>
  </head>
  <body>
    <div id="tape"></div>
    <div>
      <label id="stateLabel">State: q0 (0 steps)</label>
      <label id="headLabel">Head: 0</label>
      <button onclick="runStep()">Run Step</button>
      <button onclick="toggleAuto()">Auto Move</button>
      <button onclick="reset()">Reset</button>
    </div>
    <div>
      <input type="text" id="inputWord" placeholder="Input Word" />
      <button onclick="setInput()">Set Input</button>
    </div>
    <div id="result"></div>

    <script>
      // JavaScript код
      let tape = "1111+11 ";
      let headIndex = 0;
      let state = "q0";
      let steps = 0;
      let transitions = [
        {
          // Переход из состояния q0, если текущий символ на ленте - пробел
          currentState: "q0",
          readSymbol: " ",
          writeSymbol: " ", // Не меняем символ
          moveDirection: "Right", // Двигаемся вправо по ленте
          nextState: "q0", // Следующее состояние остается q0
        },
        {
          // Переход из состояния q0, если текущий символ на ленте - 1
          currentState: "q0",
          readSymbol: "1",
          writeSymbol: "1", // Не меняем символ
          moveDirection: "Right", // Двигаемся вправо по ленте
          nextState: "q0", // Следующее состояние остается q0
        },
        {
          // Переход из состояния q0, если текущий символ на ленте - "+"
          currentState: "q0",
          readSymbol: "+",
          writeSymbol: "1", // Заменяем "+" на "1"
          moveDirection: "Right", // Двигаемся вправо по ленте
          nextState: "q1", // Следующее состояние - q1
        },
        {
          // Переход из состояния q1, если текущий символ на ленте - 1
          currentState: "q1",
          readSymbol: "1",
          writeSymbol: "1", // Не меняем символ
          moveDirection: "Right", // Двигаемся вправо по ленте
          nextState: "q1", // Следующее состояние остается q1
        },
        {
          // Переход из состояния q1, если текущий символ на ленте - пробел
          currentState: "q1",
          readSymbol: " ",
          writeSymbol: " ", // Не меняем символ
          moveDirection: "Left", // Двигаемся влево по ленте
          nextState: "q2", // Следующее состояние - q2
        },
        {
          // Переход из состояния q2, если текущий символ на ленте - 1
          currentState: "q2",
          readSymbol: "1",
          writeSymbol: " ", // Заменяем "1" на пробел
          moveDirection: "Left", // Двигаемся влево по ленте
          nextState: "q4", // Следующее состояние - q4
        },
        {
          // Переход из состояния q4, если текущий символ на ленте - 1
          currentState: "q4",
          readSymbol: "1",
          writeSymbol: "1", // Не меняем символ
          moveDirection: "Left", // Двигаемся влево по ленте
          nextState: "q3", // Следующее состояние - q3
        },
      ];
      let timer;
      const autoMoveInterval = 500; // milliseconds

      function initializeTape() {
        let tapeDiv = document.getElementById("tape");
        for (let i = 0; i < tape.length; i++) {
          let cell = document.createElement("div");
          cell.classList.add("cell");
          cell.textContent = tape[i];
          tapeDiv.appendChild(cell);
        }
      }

      function updateTape() {
        let tapeDiv = document.getElementById("tape");
        let cells = tapeDiv.children;
        for (let i = 0; i < cells.length; i++) {
          if (i === headIndex) {
            cells[i].classList.add("head");
          } else {
            cells[i].classList.remove("head");
          }
          // Отобразить только текущий символ
          cells[i].textContent = tape[i];
        }
      }

      function updateStateLabel() {
        document.getElementById(
          "stateLabel"
        ).textContent = `State: ${state} (${steps} steps)`;
      }

      function updateHeadLabel() {
        document.getElementById("headLabel").textContent = `Head: ${headIndex}`;
      }

      function updateResultLabel() {
        let resultDiv = document.getElementById("result");
        if (state === "q3") {
          let plusIndex = tape.lastIndexOf("+");
          if (plusIndex !== -1) {
            tape =
              tape.substring(0, plusIndex + 1) + tape.substring(plusIndex + 1);
          }
          resultDiv.textContent = `Result: ${tape}`;
        } else {
          resultDiv.textContent = "";
        }
      }

      function runStep() {
        // Проверяем, находится ли машина в финальном состоянии
        if (state === "q3") {
          // Если да, то останавливаем выполнение шагов
          clearInterval(timer);
          timer = null;
          // Находим индекс последнего символа "+" на ленте
          let plusIndex = tape.lastIndexOf("+");
          if (plusIndex !== -1) {
            // Если "+" найден, заменяем его на "1"
            let tapeArray = tape.split("");
            tapeArray[plusIndex] = "1";
            tape = tapeArray.join("");
          }
          // Обновляем отображение ленты и результата
          updateTape();
          updateResultLabel();
          return;
        }

        // Получаем текущий символ на ленте
        let currentSymbol = tape[headIndex];
        // Находим подходящее правило перехода для текущего состояния и символа
        let transition = transitions.find(
          (t) => t.currentState === state && t.readSymbol === currentSymbol
        );

        if (transition) {
          // Если правило перехода найдено, обновляем символ на ленте
          let tapeArray = tape.split("");
          tapeArray[headIndex] = transition.writeSymbol;
          tape = tapeArray.join("");

          // Увеличиваем количество выполненных шагов
          steps++;

          // Перемещаем головку ленты в соответствии с указанным направлением
          if (transition.moveDirection === "Left") {
            headIndex--;
          } else {
            headIndex++;
          }

          // Обновляем текущее состояние
          state = transition.nextState;

          // Проверяем, не выходит ли головка ленты за границы ленты
          if (headIndex < 0 || headIndex >= tape.length) {
            // Если выходит, останавливаем выполнение шагов и выводим результат
            clearInterval(timer);
            timer = null;
            alert("Result: " + tape);
            return;
          }
        } else {
          // Если правило перехода не найдено, останавливаем выполнение шагов и выводим предупреждение
          clearInterval(timer);
          timer = null;
          alert("No transition rule found for current state and symbol.");
          return;
        }

        // Обновляем отображение ленты, текущего состояния, позиции головки и результата
        updateTape();
        updateStateLabel();
        updateHeadLabel();
        updateResultLabel();
      }

      function toggleAuto() {
        if (timer) {
          clearInterval(timer);
          timer = null;
        } else {
          timer = setInterval(runStep, autoMoveInterval);
        }
      }

      function reset() {
        tape = "1111+11 ";
        headIndex = 0;
        state = "q0";
        steps = 0;
        clearInterval(timer);
        timer = null;
        let tapeDiv = document.getElementById("tape");
        tapeDiv.innerHTML = ""; // Очистка ленты
        initializeTape(); // Перерисовка ленты с новым вводом
        updateStateLabel();
        updateHeadLabel();
        updateResultLabel();
      }

      function setInput() {
        let inputWord = document.getElementById("inputWord").value.trim();
        if (inputWord === "") {
          alert("Please enter an input word.");
          return;
        }
        tape = inputWord + " ";
        headIndex = 0;
        state = "q0";
        steps = 0;
        clearInterval(timer);
        timer = null;
        let tapeDiv = document.getElementById("tape");
        tapeDiv.innerHTML = ""; // Очистка ленты
        initializeTape(); // Перерисовка ленты с новым вводом
        updateStateLabel();
        updateHeadLabel();
        updateResultLabel();
      }

      // Initialize on page load
      window.onload = function () {
        initializeTape();
        updateStateLabel();
        updateHeadLabel();
        updateResultLabel();
      };
    </script>
  </body>
</html>
