import tkinter as tk

# Определяем конечный автомат для светофора с 4 состояниями
class TrafficLightFSM:
    def __init__(self):
        # Состояния: Красный, Красный и Желтый, Зеленый, Желтый
        self.states = ["Red", "RedYellow", "Green", "Yellow"]
        self.current_state = 0  # Начальное состояние (Red)
    
    def next_state(self):
        self.current_state = (self.current_state + 1) % len(self.states)
        return self.states[self.current_state]
    
    def get_current_state(self):
        return self.states[self.current_state]

# Основное приложение с Tkinter
class TrafficLightApp(tk.Tk):
    def __init__(self, fsm):
        super().__init__()
        self.fsm = fsm
        self.title("Светофор")
        self.geometry("200x400")
        self.configure(bg="white")
        
        # Создаем холст для отрисовки светофора
        self.canvas = tk.Canvas(self, width=100, height=300)
        self.canvas.pack(pady=20)
        
        # Отрисовываем круги для сигналов светофора
        self.red_light = self.canvas.create_oval(25, 25, 75, 75, fill="gray")
        self.green_light = self.canvas.create_oval(25, 225, 75, 275, fill="gray")
        self.yellow_light = self.canvas.create_oval(25, 125, 75, 175, fill="gray")
        
        # Запускаем процесс смены состояний
        self.update_lights()

    def update_lights(self):
        # Получаем текущее состояние автомата
        state = self.fsm.get_current_state()

        # Устанавливаем цвета на основании текущего состояния
        if state == "Red":
            self.canvas.itemconfig(self.red_light, fill="red")
            self.canvas.itemconfig(self.yellow_light, fill="gray")
            self.canvas.itemconfig(self.green_light, fill="gray")
        elif state == "RedYellow":
            self.canvas.itemconfig(self.red_light, fill="red")
            self.canvas.itemconfig(self.yellow_light, fill="yellow")
            self.canvas.itemconfig(self.green_light, fill="gray")
        elif state == "Green":
            self.canvas.itemconfig(self.red_light, fill="gray")
            self.canvas.itemconfig(self.yellow_light, fill="gray")
            self.canvas.itemconfig(self.green_light, fill="green")
        elif state == "Yellow":
            self.canvas.itemconfig(self.red_light, fill="gray")
            self.canvas.itemconfig(self.yellow_light, fill="yellow")
            self.canvas.itemconfig(self.green_light, fill="gray")
        
        # Переход в следующее состояние через 1 секунду
        self.fsm.next_state()
        self.after(1000, self.update_lights)  # обновление каждые 1000 мс (1 секунда)

# Инициализация конечного автомата и приложения
if __name__ == "__main__":
    fsm = TrafficLightFSM()  # Создаем конечный автомат для светофора
    app = TrafficLightApp(fsm)  # Создаем приложение
    app.mainloop()  # Запускаем цикл обработки событий Tkinter
