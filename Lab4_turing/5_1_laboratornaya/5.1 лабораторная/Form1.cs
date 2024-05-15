using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Windows.Forms;


namespace Lab5_TuringMachineGUI_v1
{
    public partial class Form1 : Form
    {
        private TuringMachine turingMachine;
        private PictureBox tapePictureBox;
        private Button runButton;
        private Label stateLabel;
        private Label headLabel;
        private Timer timer;
        private const int AutoMoveInterval = 700; // Интервал автоматического движения головки (в миллисекундах)

        public Form1()
        {
            InitializeComponent();
            InitializeTuringMachine();
            InitializeTimer();

            //GenerateStateGraph();
            //UpdateGraphImage();
        }

        private void InitializeTimer()
        {
            timer = new Timer();
            timer.Interval = AutoMoveInterval;
            timer.Tick += Timer_Tick;
        }

        private void InitializeTuringMachine()
        {
            // Создание экземпляра машины Тьюринга
            turingMachine = new TuringMachine();

            // Задание начальной ленты
            turingMachine.Tape = " ++++ ";
            turingMachine.HeadIndex = 1;

            // Задание начального состояния
            turingMachine.State = "q1";

            // Задание правил перехода
            turingMachine.Transitions = new List<Transition>
            {
                // Правила переходов с "+" на "-"
                new Transition("q0", ' ', ' ', Direction.None, "q0"),
                new Transition("q1", '+', '+', Direction.Right, "q1"),
                new Transition("q2", '+', '+', Direction.Left, "q3"),
                new Transition("q3", '+', '-', Direction.Left, "q2"),
                new Transition("q1", ' ', ' ', Direction.Left, "q2"),
                new Transition("q2", ' ', ' ', Direction.None, "q0"),
                new Transition("q3", ' ', ' ', Direction.None, "q0"),
            };
            // Обновление отображения
            UpdateTapePictureBox();
            UpdateStateLabel();
            UpdateHeadLabel();
            GenerateStateGraph();
            UpdateGraphImage(); 
        }


        private void Timer_Tick(object sender, EventArgs e)
        {
            // Выполнение одного шага машины Тьюринга
            turingMachine.Step(this.timer);
            // Обновление отображения
            UpdateTapePictureBox();
            UpdateStateLabel();
            UpdateHeadLabel();
            GenerateStateGraph();
            UpdateGraphImage();

            if (turingMachine.State == "q0")
            {
                // Остановить таймер
                timer.Stop();
                resultLabel.Text = "Результат: " + turingMachine.Tape;
                runButton.Enabled = false;
                autoMoveButton.Enabled = false;
                //Debug.WriteLine("Генерация графа после достижения q0");
                return;
            }

        }
        
        private void RunButton_Click(object sender, EventArgs e)
        {
            if (timer.Enabled)
            {
                timer.Stop();
                return;
            }

            // Выполнение одного шага машины Тьюринга
            turingMachine.Step(this.timer);
            // Обновление отображения
            UpdateTapePictureBox();
            UpdateStateLabel();
            UpdateHeadLabel();
            GenerateStateGraph();
            UpdateGraphImage();

            if (turingMachine.State == "q0")
            {
                // Остановить таймер
                timer.Stop();
                resultLabel.Text = "Результат: " + turingMachine.Tape;
                //Debug.WriteLine("Генерация графа после достижения q0");
                runButton.Enabled = false;
                autoMoveButton.Enabled = false;
                return;
            }

        }
        private void UpdateGraphImage()
        {
            // Путь к файлу с изображением графа
            string imagePath = "state_graph.png";

            // Проверяем, существует ли файл с изображением графа
            if (File.Exists(imagePath))
            {
                // Отображаем изображение на PictureBox2
                using (FileStream stream = new FileStream(imagePath, FileMode.Open))
                {
                    pictureBox2.Image = Image.FromStream(stream);
                }
            }
            else
            {
                // Выводим сообщение об ошибке, если файл с изображением не найден
                MessageBox.Show("Файл с изображением графа не найден.");
            }
        }

        private void GenerateStateGraph()
        {
            string dotFilePath = "state_graph.dot";

            using (StreamWriter writer = new StreamWriter(dotFilePath))
            {
                writer.WriteLine("digraph StateGraph {");

                foreach (Transition transition in turingMachine.Transitions)
                {
                    if (transition.CurrentState == turingMachine.State)
                    {
                        writer.WriteLine($"    {transition.CurrentState} [style=filled, fillcolor=green];");
                    }

                    writer.WriteLine($"    {transition.CurrentState} -> {transition.NextState} [label=\"{transition.ReadSymbol} -> {transition.WriteSymbol}, {transition.MoveDirection}\"];");
                }

                writer.WriteLine("}");
            }

            ProcessStartInfo startInfo = new ProcessStartInfo
            {
                FileName = "state_graph.dot",
                Arguments = $"-Tpng {dotFilePath} -o state_graph.png",
                CreateNoWindow = true,
                UseShellExecute = false
            };

            Process process = Process.Start(startInfo);
            process.WaitForExit(); // Ждем завершения процесса создания изображения графа

            UpdateGraphImage(); // Обновляем изображение после завершения процесса
        }



        private void UpdateTapePictureBox()
        {
            // Очистка PictureBox
            tapePictureBox.Image = new Bitmap(tapePictureBox.Width, tapePictureBox.Height);
            Graphics g = Graphics.FromImage(tapePictureBox.Image);
            g.Clear(Color.White);

            // Получение информации о ленте и головке
            string tape = turingMachine.Tape;
            int headIndex = turingMachine.HeadIndex;

            // Отрисовка ленты
            int cellWidth = tapePictureBox.Width / (tape.Length + 1);
            int cellHeight = tapePictureBox.Height;
            for (int i = 0; i < tape.Length; i++)
            {
                Rectangle cellRect = new Rectangle(i * cellWidth, 0, cellWidth, cellHeight);
                g.DrawRectangle(Pens.Black, cellRect);
                g.DrawString(tape[i].ToString(), Font, Brushes.Black, cellRect, new StringFormat { Alignment = StringAlignment.Center, LineAlignment = StringAlignment.Center });
            }

            // Отрисовка головки
            Rectangle headRect = new Rectangle(headIndex * cellWidth, 0, cellWidth, cellHeight);
            Color transparentRed = Color.FromArgb(128, Color.Gray); // Полупрозрачный красный цвет
            using (Brush brush = new SolidBrush(transparentRed))
            {
                g.FillRectangle(brush, headRect);
            }
        }

        private void UpdateStateLabel()
        {
            stateLabel.Text = "Состояние: " + turingMachine.State + " (" + turingMachine.Steps + " шагов)";
        }

        private void UpdateHeadLabel()
        {
            headLabel.Text = "Позиция головки автомата: " + turingMachine.HeadIndex;
        }

        private void autoMoveButton_Click(object sender, EventArgs e)
        {
            timer.Start();
        }

        private void buttonInput_Click(object sender, EventArgs e)
        {
            // Получение входного слова из TextBox
            string inputWord = inputTextBox.Text;

            // Проверка, что входное слово не является пустым
            if (string.IsNullOrWhiteSpace(inputWord))
            {
                MessageBox.Show("Введите входное слово.");
                return;
            }

            // Обнуление состояния машины Тьюринга
            turingMachine.Reset();

            // Задание начальной ленты
            turingMachine.Tape = ' ' + inputWord + ' ';
            runButton.Enabled = true;
            autoMoveButton.Enabled = true;
            // Обновление положения головки
            turingMachine.HeadIndex = 1;

            // Обновление отображения
            UpdateTapePictureBox();
            UpdateStateLabel();
            UpdateHeadLabel();
            InitializeTimer();
            GenerateStateGraph();
            UpdateGraphImage(); // Обновляем изображение после завершения процесса
        }

        private void resultLabel_Click(object sender, EventArgs e)
        {

        }

        private void inputTextBox_TextChanged(object sender, EventArgs e)
        {

        }
    }

    public enum Direction
    {
        Left,
        Right,
        None
    }


    public class Transition
    {
        public string CurrentState { get; set; } // Текущее состояние автомата
        public char ReadSymbol { get; set; } // Символ, считанный с ленты
        public char WriteSymbol { get; set; } // Символ, который нужно записать на ленту
        public Direction MoveDirection { get; set; } // Направление движения головки ленты
        public string NextState { get; set; } // Следующее состояние автомата

        public Transition(string currentState, char readSymbol, char writeSymbol, Direction moveDirection, string nextState)
        {
            CurrentState = currentState;
            ReadSymbol = readSymbol;
            WriteSymbol = writeSymbol;
            MoveDirection = moveDirection;
            NextState = nextState;
        }
    }

    public class TuringMachine
    {
        private bool errorShown;

        public string Tape { get; set; } // Лента автомата
        public int HeadIndex { get; set; } // Текущий индекс головки ленты
        public string State { get; set; } // Текущее состояние автомата

        public int Steps { get; set; } // Количество выполненных шагов автомата
        public List<Transition> Transitions { get; set; } // Список правил перехода для автомата

        public void Reset()
        {
            Tape = string.Empty; // Сбросить ленту, установив пустую строку
            HeadIndex = 1; // Сбросить индекс головки ленты, установив 0
            State = "q1"; // Сбросить состояние автомата, установив начальное состояние "q0"
            Steps = 0; // Сбросить количество шагов, установив 0
            errorShown = false;
        }

        public void Step(Timer timer)
        {
            // Получить текущий символ на ленте
            char currentSymbol = Tape[HeadIndex];

            // Найти соответствующее правило перехода
            Transition transition = Transitions.FirstOrDefault(t => t.CurrentState == State && t.ReadSymbol == currentSymbol);

            if (transition != null)
            {
                // Записать новый символ на ленту
                StringBuilder tapeBuilder = new StringBuilder(Tape);
                tapeBuilder[HeadIndex] = transition.WriteSymbol;
                Tape = tapeBuilder.ToString();

                // Увеличить количество шагов
                Steps++;

                // Сдвинуть головку ленты в указанном направлении
                if (transition.MoveDirection == Direction.Left)
                {
                    HeadIndex--;
                }
                else if (transition.MoveDirection == Direction.Right)
                {
                    HeadIndex++;
                }


                // Изменить текущее состояние
                State = transition.NextState;

                // Проверка, если головка выходит за пределы ленты
                if (HeadIndex < 0 || HeadIndex >= Tape.Length)
                {
                    MessageBox.Show("Результат: " + Tape);
                    return;
                }
            }
            else if (!errorShown) // Проверка, было ли уже показано сообщение об ошибке
            {
                timer.Stop(); // Останавливаем таймер при ошибке
                errorShown = true; // Устанавливаем флаг, чтобы сообщение об ошибке больше не показывалось

                MessageBox.Show("Не найдено правило перехода для текущего состояния и символа.");

                return;
            }
        }
    }

    }
