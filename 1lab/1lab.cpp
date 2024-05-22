#include <iostream>
#include <string>
#include <vector>
#include <random>
#include <algorithm>
#include <fstream>
#include <map>
#include <stack>
#include <unordered_set>
#include <unordered_map>
#include <fstream>
#include <sstream>
#include <cstdlib>

using namespace std;

/// <summary>
/// класс правило
/// </summary>

class Rule {
public:
    string A;
    string B;
    char weight;
    bool isLooped;

    Rule(string a, string b, char w = '1', bool l = false) {
        A = a;
        B = b;
        weight = w;
        isLooped = l;
    }
};




/// <summary>
/// класс формального языка с леволинейной грамматикой и проверкой на зацикливание
/// </summary>
class FormalLanguage {
private:
    /// <summary>
    /// вектор правил языка
    /// </summary>
    vector<Rule> rules;

    /// <summary>
    /// Максимально количество повторений
    /// </summary>
    unsigned MaxRepetitionsCount;

    /// <summary>
    /// проверка правила на зацикливание
    /// </summary>
    /// <param name="input"> строка, к которой применяется правило </param>
    /// <param name="rule"> правило </param>
    /// <param name="count"> количество допустимых повторений </param>
    /// <returns></returns>
    bool checkLoop(string input, Rule rule, unsigned count = 10) {
        for (int i = 0; i < count; i++)
        {
            string A = rule.A;
            string B = rule.B;
            size_t pos = input.find(A);
            if (pos != string::npos) {
                input.replace(pos, A.length(), B);
            }
            else return false;
        }
        return true;
    }

    /// <summary>
    /// обновление состояния isLooped всех правил
    /// </summary>
    void RefreshRules() {
        for (Rule& rule : rules) {
            rule.isLooped = false;
        }
    }

public:

    void PrintRules() {
        cout << "Правила для языка:" << endl;
        for (int i = 0; i < rules.size(); i++) {
            cout << rules[i].A << " -> " << rules[i].B << " (переход: " << rules[i].weight << ")" << endl;
        }
    }

    /// <summary>
    /// конструктор
    /// </summary>
    /// <param name="rules_"> вектор правил </param>
    /// <param name="count"> максимальное количество повторений - по дефолту 10000</param>
    FormalLanguage(vector<Rule> rules_, unsigned count = 100) {
        rules = rules_;
        MaxRepetitionsCount = count;
    }



    void printGraphs(string name) {
        // Создание временного файла для сохранения описания графа в формате DOT
        std::ofstream dotFile("graph.dot");

        // Запись заголовка файла DOT
        dotFile << "digraph G {\n";

        // Запись описания каждого правила в формате DOT
        for (const auto& rule : rules) {
            dotFile << "    " << rule.A << " -> " << rule.B << " [label=\"" << rule.weight << "\"];\n";
        }


        // Запись завершающего символа в файл DOT
        dotFile << "}\n";

        // Закрытие файла DOT
        dotFile.close();

        // Создание команды для вызова Graphviz и генерации графического файла
        std::string command = "dot -Tpng -o "+ name+ ".png graph.dot";

        // Выполнение команды с помощью системной функции
        std::system(command.c_str());

        // Удаление временного файла DOT
        std::remove("graph.dot");

        // Вывод сообщения о завершении операции
        std::cout << "Графы успешно выведены в файл" + name + ".png" << std::endl;
    }

    // Метод для удаления недостижимых правил языка
    // Метод удаления недостижимых состояний из состояния startState
    void deleteUnreachable(char startState) {
        unordered_set<char> result;// Множество достижимых состояний
        stack<char> buffer;// Буфер для обхода состояний

        result.insert(startState); // Добавляем начальное состояние в множество достижимых состояний
        buffer.push(startState); // Добавляем начальное состояние в буфер

        while (!buffer.empty()) {
            char currentState = buffer.top();// Получаем текущее состояние из вершины буфера
            buffer.pop();// Удаляем текущее состояние из буфера

            // Перебираем все правила
            for (const auto& rule : rules) {
                // Если левая часть правила соответствует текущему состоянию
                if (rule.A[0] == currentState) {
                    // Перебираем символы правой части
                    for (char c : rule.B) {
                        // Если символ еще не был добавлен в множество достижимых состояний
                        if (result.find(c) == result.end()) {
                            result.insert(c);// Добавляем символ в множество достижимых состояний
                            buffer.push(c);// Добавляем символ в буфер для обхода
                        }
                    }
                }
            }
        }
        // Удаляем недостижимые правила из общего списка правил
        rules.erase(remove_if(rules.begin(), rules.end(), [&](const Rule& rule) {
            return result.find(rule.A[0]) == result.end();
        }), rules.end());
    }

    // удаление эквивалентных состояний
    void deleteEquivalent() {
        //вектор для хранения уникальных правил
        vector<Rule> result;

        // Функция для проверки эквивалентности двух правил
        auto isEquivalent = [&](const Rule& rule1, const Rule& rule2) {
            return rule1.B == rule2.B;
        };
        // Перебор всех правил в исходном векторе
        for (const auto& rule : rules) {
            bool isDuplicate = false;
            // Проверка текущего правила на эквивалентность с уже добавленными уникальными правилами
            for (const auto& uniqueRule : result) {
                // Если правило эквивалентно другому правилу, считаем его дубликатом
                if (isEquivalent(rule, uniqueRule)) {
                    isDuplicate = true;
                    break;
                }
            }
            // Если текущее правило не является дубликатом, добавляем его в вектор уникальных правил
            if (!isDuplicate) {
                result.push_back(rule);
            }
        }
        // Очищаем исходный вектор правил
        rules.clear();
        // Копируем уникальные правила из вектора result обратно в исходный вектор rules
        for (const auto& rule : result) {
            rules.push_back(rule);
        }
    }

    /// <summary>
    /// функция перевода строки на формальный язык
    /// </summary>
    /// <param name="text"> входная строка </param>
    /// <returns> выходная цепочка </returns>
    string Translate(string text) {
        int count = 0; /// счетчик максимального количества повторений
        bool isEnd = false; /// ни одно из правил неприменимо
        /// повторяем, пока не достигнем максимального количества повторений
        while (count < MaxRepetitionsCount) {
            if (isEnd) break; /// выход, если правила не применимы
            count++; /// инкремент счетчика
            isEnd = true; /// предполагаем, что это последняя итерация
            for (Rule& rule : rules) { /// проходимся по всем правилам отдельно
                if (!rule.isLooped) { /// приводит ли правило к зацикливанию
                    string A = rule.A; /// получаем символы из правила
                    string B = rule.B;

                    size_t pos = text.find(A); /// ищем из А
                    //cout << text << endl;
                    if (pos != string::npos) { /// если порождающий найден
                        if (checkLoop(text, rule)) { /// проверяем на зацикливание
                            rule.isLooped = true;
                        }
                        else { /// если зацикливания нет
                            text.replace(pos, A.length(), B); /// заменяем символы
                            isEnd = false; /// для следующей итерации обновляем
                            break;/// выход
                        }
                    }
                }
                else { /// правило приводит к зацикливанию
                    rule.isLooped = true;
                }
            }
        }
        RefreshRules(); /// обновление isLooped для правил перед выходом
        return text; /// возврат выходной цепочки
    }

    string OutputLeft(vector<string>& transformations)
    {
        transformations.clear();
        string result = "S";
        int count = 0;

        while (count < MaxRepetitionsCount)
        {
            size_t pos = string::npos;

            // найдем крайний левый нетерминальный символ в цепочке
            for (const Rule& rule : rules)
            {
                string key = rule.A;
                size_t findPos = result.find(key);
                if ((pos > findPos || pos == string::npos) && findPos != string::npos)
                {
                    pos = findPos;
                    break;
                }
            }
            // если не найдено ниодного подходящего правила - выходим
            if (pos == string::npos)
            {
                break;
            }
            // для правого
            // найдем все правила подходящие для крайнего левого нетерминального символа
            std::vector<Rule> rules_;
            for (const Rule& rule : rules) {
                std::string key = rule.A;
                if (pos == result.find(key)) {
                    rules_.push_back(rule);
                }
            }

            std::random_device rd;
            std::mt19937 gen(rd());
            std::uniform_int_distribution<> dis(0, rules_.size() - 1);
            int index = dis(gen);
            Rule r = rules_[index];

            size_t p = result.find(r.A);
            result.replace(p, r.A.length(), r.B);
            //cout << result << endl;
            transformations.push_back("( " + r.A + " --> " + r.B + " ): " + result);
            count++;
        }
        //cout << result << endl;
        return result;
    }

    string OutputLeft_Equivalence()
    {
        string result = "S";
        int count = 0;

        while (count < MaxRepetitionsCount)
        {
            size_t pos = string::npos;

            // найдем крайний левый нетерминальный символ в цепочке
            for (const Rule& rule : rules)
            {
                string key = rule.A;
                size_t findPos = result.find(key);
                if ((pos > findPos || pos == string::npos) && findPos != string::npos)
                {
                    pos = findPos;
                    break;
                }
            }
            // если не найдено ниодного подходящего правила - выходим
            if (pos == string::npos)
            {
                break;
            }
            // для правого
            // найдем все правила подходящие для крайнего левого нетерминального символа
            std::vector<Rule> rules_;
            for (const Rule& rule : rules) {
                std::string key = rule.A;
                if (pos == result.find(key)) {
                    rules_.push_back(rule);
                }
            }

            std::random_device rd;
            std::mt19937 gen(rd());
            std::uniform_int_distribution<> dis(0, rules_.size() - 1);
            int index = dis(gen);
            Rule r = rules_[index];

            size_t p = result.find(r.A);
            result.replace(p, r.A.length(), r.B);

            count++;
        }
        //cout << result << endl;
        return result;
    }


    string Transformations(string chain_) {
        string buf;
        string result;
        vector<string> transformations;
        bool found = false;
        int counter = 0;
        while (!found) {
            buf = this->OutputLeft(transformations);
            counter++;
            if (counter == 10000000) return "Цепочка не построена. Попробуйте ещё раз\n";
            if (buf == chain_) found = true;
        }

        for (int i = 0; i < transformations.size(); i++)
        {
            result += transformations[i] + "\n";
        }
        result.insert(0, "Начальный символ: S\n");

        return result;
    }
};

//void FillVectorWithUniqueChars(string inputString, vector<char>& vector)
//{
//    for (char c : inputString) {
//        if (std::find(vector.begin(), vector.end(), c) == vector.end()) {
//            vector.push_back(c);
//        }
//    }
//}
//
//string equivalence(FormalLanguage fl1, FormalLanguage fl2) {
//    vector<char> alphabet1, alphabet2;
//    string buf1, buf2;
//    vector<string> transformations;
//    for (int i = 0; i < 10000; i++)
//    {
//        buf1 = fl1.OutputLeft_Equivalence();
//        buf2 = fl2.OutputLeft_Equivalence();
//        FillVectorWithUniqueChars(buf1, alphabet1);
//        FillVectorWithUniqueChars(buf2, alphabet2);
//    }
//    
//    sort(alphabet1.begin(), alphabet1.end());
//    sort(alphabet2.begin(), alphabet2.end());
//    cout << endl << "Символы в первом языке: ";
//    for (int i = 0; i < alphabet1.size(); i++)
//    {
//        cout  << alphabet1[i] << " ";
//    }
//    cout << endl << "Символы во втором языке: ";
//    for (int i = 0; i < alphabet2.size(); i++)
//    {
//        cout  << alphabet2[i] << " ";
//    }
//    cout << endl;
//    bool isEqual = equal(alphabet1.begin(), alphabet1.end(), alphabet2.begin());
//    if (isEqual) {
//        return "Грамматики эквивалентны";
//    }
//    else {
//        return "Грамматики не эквивалентны";
//    }
//}
//
//
//class Grammar {
//public:
//    vector<string> Nonterminal;
//    vector<string> Terminal;
//    vector<Rule> P;
//    string S;
//
//    Grammar(vector<string> vn, vector<string> vt, vector<Rule> rules, string s = "S") : Nonterminal(vn), Terminal(vt), P(rules), S(s) {}
//
//    string GetTypeGrammar() {
//        bool isTypeOne = true;
//        bool isTypeTwo = true;
//        bool isTypeThree = true;
//
//        bool isEachTermPosBigger = true;
//        bool isEachTermPosSmaller = true;
//
//        for (const Rule& r : P) {
//            isTypeOne &= r.A.length() <= r.B.length();
//
//            for (const string& vt : Terminal) {
//                isTypeTwo &= r.A.find(vt) == string::npos;
//            }
//
//            if (isEachTermPosBigger || isEachTermPosSmaller) {
//                vector<int> terminalPositions;
//                vector<int> nonTerminalPositions;
//                for (const string& vn : Nonterminal) {
//                    int temp = r.B.find(vn);
//                    if (temp != -1) {
//                        nonTerminalPositions.push_back(temp);
//                    }
//                }
//                for (const string& vt : Terminal) {
//                    int temp = r.B.find(vt);
//                    if (temp != -1) {
//                        terminalPositions.push_back(temp);
//                    }
//                }
//                for (int pos : terminalPositions) {
//                    for (int posNonTerm : nonTerminalPositions) {
//                        isEachTermPosBigger &= pos > posNonTerm;
//                        isEachTermPosSmaller &= pos < posNonTerm;
//                    }
//                }
//                if (!isEachTermPosBigger && !isEachTermPosSmaller) {
//                    isTypeThree = false;
//                }
//            }
//        }
//
//        string res = "0";
//        if (isTypeOne) res += " 1";
//        if (isTypeTwo) res += " 2";
//        if (isTypeThree) res += " 3";
//        return res;
//    }
//
//    string MakeTree(string text) {
//        int maxCount = 10000;
//        int count = 0;
//        vector<string> tree;
//        tree.push_back(text);
//
//        while (count < maxCount) {
//            for (const Rule& rule : P) {
//                string key = rule.A;
//                string value = rule.B;
//
//                int pos = text.find(value);
//                if (pos != -1) {
//                    text.replace(pos, value.length(), key);
//
//                    string separator = "|";
//                    for (int i = 0; i < pos; i++) {
//                        separator = " " + separator;
//                    }
//                    tree.push_back(separator);
//                    tree.push_back(text);
//                }
//            }
//            count++;
//        }
//
//        for (auto it = tree.rbegin(); it != tree.rend(); ++it) {
//            cout << *it << endl;
//        }
//        return text;
//    }
//
//};
//
//
//enum State { H, N, S, ER };
//map<State, string> StateToString = { { H, "H" },
//                                     { N, "N" },  
//                                     { S, "S" },
//                                     { ER, "ER" }
//};
//
//// Function to convert a Color enum value to its string 
//// representation 
//string enumToString(State s)
//{
//    return StateToString[s];
//}
//
//static void Analizator(string text)
//{
//    int b, c;
//    State now = H;
//    int count = 0;
//    string res = "";
//    do
//    {
//        //проверка выхода за пределы индексации
//        if (count < text.length())
//        {
//            switch (now)
//            {
//            case H:
//            {
//                c = text[count];
//                if (text[count] == '0') {
//                    now = N;
//                    b = c - '0';
//                    c = text[count + 1];
//                }
//                else if (text[count] == '1') {
//                    now = N;
//                    b = c - '0';
//                    c = text[count + 1];
//                }
//                else if (text[count] == '|') now = S;
//                else {
//                    now = H;
//                    c = text[count + 1];
//                }
//                break;
//            }
//            case N:
//            {
//                if (text[count] == '0') {
//                    now = N;
//                    b = 2 * b + c - '0';
//                    c = text[count + 1];
//                }
//                else if (text[count] == '1') {
//                    now = N;
//
//                    b = 2 * b + c - '0';
//                    c = text[count + 1];
//                }
//                else {
//                    now = H;
//                    c = text[count + 1];
//                    cout << b;
//                }
//                break;
//            }
//            case S:
//            {
//                break;
//            }
//            default:
//                break;
//            }
//
//            res += enumToString(now);
//            res += "";
//            count++;
//        }
//        else break;
//    } while (now != ER);
//    cout << endl << "Цепочка состояний: " << res;
//
//    //if (enumToString(now) == "S") cout << endl << "Цепочка " << text << " принадлежит данному языку" << endl << endl;
//
//    //else cout << endl << "Цепочка " << text << " не принадлежит данному языку" << endl << endl;
//}

void GenerateGraphML(const vector<Rule>& rules, string fileName) {
    unordered_set<string> nodes;
    unordered_map<string, vector<char>> edgeWeights;

    ofstream file(fileName + ".graphml");
    if (!file) {
        cout << "Failed to create the file." << endl;
        return;
    }

    file << "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" << endl;
    file << "<graphml xmlns=\"http://graphml.graphdrawing.org/xmlns\"" << endl;
    file << "         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"" << endl;
    file << "         xsi:schemaLocation=\"http://graphml.graphdrawing.org/xmlns" << endl;
    file << "         http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd\">" << endl;
    file << "    <graph id=\"G\" edgedefault=\"directed\">" << endl;

    for (const auto& rule : rules) {
        nodes.insert(rule.A);
        nodes.insert(rule.B);

        string edgeId = rule.A + "_" + rule.B;
        edgeWeights[edgeId].push_back(rule.weight);

        file << "        <node id=\"" << rule.A << "\"/>" << endl;
        file << "        <node id=\"" << rule.B << "\"/>" << endl;
        file << "        <edge id=\"" << edgeId << "\" source=\"" << rule.A << "\" target=\"" << rule.B << "\">" << endl;
        file << "            <data key=\"weight\">" << rule.weight << "</data>" << endl;
        file << "        </edge>" << endl;
    }

    for (auto it = edgeWeights.begin(); it != edgeWeights.end(); ++it) {
        const string& edgeId = it->first;
        const vector<char>& weights = it->second;
        if (weights.size() > 1) {
            for (const auto& weight : weights) {
                file << "        <edge id=\"" << edgeId << "_copy\" source=\"" << edgeId << "_source\" target=\"" << edgeId << "_target\">" << endl;
                file << "            <data key=\"weight\">" << weight << "</data>" << endl;
                file << "        </edge>" << endl;
            }
            file << "        <node id=\"" << edgeId << "_source\"/>" << endl;
            file << "        <node id=\"" << edgeId << "_target\"/>" << endl;
        }
    }

    file << "    </graph>" << endl;
    file << "    <key id=\"weight\" for=\"edge\" attr.name=\"weight\" attr.type=\"string\"/>" << endl;
    file << "</graphml>" << endl;

    file.close();

    cout << "Файл создан" << endl;
}


int main() {
    setlocale(LC_ALL, "ru");
    vector<Rule> dict;
    string way;
    //dict = {
    //    Rule("M", "F" ,'^'),
    //    Rule("M", "C", '0'),
    //    Rule("M", "X", '1'),
    //    Rule("C", "N", '0'),
    //    Rule("N", "M", '1'),
    //    Rule("B", "N", '!'),
    //    Rule("B", "C", '&'),
    //    Rule("X", "S", '0'),
    //    Rule("S", "M", '1'),
    //    Rule("Z", "X", 'v'),
    //    Rule("Z", "S", '^')
    //};
    dict = {
        Rule("S", "A", '0'),
        Rule("S", "B", '1'),
        Rule("A", "E", '*'),
        Rule("B", "D", '/'),
        Rule("C", "B", 'a'),
        Rule("C", "E", 'b'),
        Rule("D", "E", 'b'),
        Rule("D", "F", '0'),
        Rule("D", "G", 'a'),
        Rule("E", "D", 'b'),
        Rule("E", "G", 'a'),
        Rule("E", "N", '0'),
        Rule("F", "D", '-'),
        Rule("N", "E", '-'),
    };

    FormalLanguage fl(dict);
    cout << "Правила автомата" << endl;
    fl.PrintRules();
    fl.printGraphs("1st");
    //GenerateGraphML(dict, "1");

    // Удаление недостижимых состояний
    fl.deleteUnreachable('S');
    cout << "Правила  после удаления недостижимых состоянии" << endl;
    fl.PrintRules();
    fl.printGraphs("2nd");
    //GenerateGraphML(dict, "2");

    // Удаление эквивалентных состояний
    fl.deleteEquivalent();
    cout << "Правила после удаления эквивалентных состоянии" << endl;
    fl.PrintRules();
    fl.printGraphs("3rd");
    //GenerateGraphML(dict, "3");

    //generate_csv_graph(dict);
    //GenerateGraphML(dict);

    return 0;
}