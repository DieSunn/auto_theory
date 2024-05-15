# Функция для обработки файла, принимает имена входного и выходного файлов
def process_file(input_file_name, output_file_name):
    try:
        # Открываем входной и выходной файлы
        with open(input_file_name, 'r') as input_file, open(output_file_name, 'w') as output_file:
            # Устанавливаем начальное состояние и другие переменные
            state = 'Normal_mode'
            ignore_next_char = False

            # Запускаем бесконечный цикл для чтения файла по символам
            while True:
                char = input_file.read(1)
                # Если символа нет, выходим из цикла
                if not char:
                    break

                # Проверяем текущее состояние
                if state == 'Normal_mode':
                    # Если символ -, проверяем следующий символ
                    if char == '-':
                        next_char = input_file.read(1)
                        # Если следующий символ -, переходим в режим однострочного комментария
                        if next_char == '-':
                            state = 'Oneliner'
                        # Иначе записываем символ в выходной файл
                        else:
                            output_file.write(char)
                    # Если символ {, проверяем следующий символ
                    elif char == '{':
                        next_char = input_file.read(1)
                        # Если следующий символ -, переходим в режим многострочного комментария
                        if next_char == '-':
                            state = 'Multiliner'
                        # Иначе записываем символ в выходной файл
                        else:
                            output_file.write(char)
                    # Если символ ', переходим в режим строкового литерала
                    elif char == "'":
                        state = 'String_literal'
                    # Иначе записываем символ в выходной файл
                    else:
                        output_file.write(char)
                # Если находимся в режиме однострочного комментария
                elif state == 'Oneliner':
                    # Если символ - перевод строки, возвращаемся в нормальный режим
                    if char == '\n':
                        state = 'Normal_mode'
                # Если находимся в режиме многострочного комментария
                elif state == 'Multiliner':
                    # Если символ -}, возвращаемся в нормальный режим
                    if char == '-':
                        next_char = input_file.read(1)
                        if next_char == '}':
                            state = 'Normal_mode'
                # Если находимся в режиме строкового литерала
                elif state == 'String_literal':
                    # Если следующий символ нужно игнорировать, переходим в нормальный режим
                    if ignore_next_char:
                        ignore_next_char = False
                    else:
                        # Если символ ', возвращаемся в нормальный режим
                        if char == "'":
                            state = 'Normal_mode'
                        # Иначе проверяем, нужно ли игнорировать следующий символ
                        else:
                            ignore_next_char = (char == '\\')
    # Обрабатываем возможное исключение, если файлы не могут быть открыты
    except FileNotFoundError:
        print("Failed to open input file or output file.")

    # Удаление последней одинарной кавычки, если программа завершилась в режиме строкового литерала
    if state == 'String_literal':
        with open(output_file_name, 'a') as output_file:
            output_file.write("'")


# Функция для запуска обработки файлов
def main():
    input_file_name = "input2.txt"
    output_file_name = "output.txt"
    process_file(input_file_name, output_file_name)
    print("Comments removed successfully.")


# Запускаем функцию main при запуске скрипта
if __name__ == "__main__":
    main()
