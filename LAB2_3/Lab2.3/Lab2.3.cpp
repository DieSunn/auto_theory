#include <iostream>
#include "../Lib/NFA_to_DFA.h"
#include "../Lib/FormalLanguage.h"
#include "../Lib/Rule.h"

using namespace std;

enum State { H, A1, B1, B0, C0, S, ER };
// ER состояние ошибки

void Analizator(const string& text) {
    State now = H;
    int count = 0;
    string res = "";

    while (count < text.length()) {
        switch (now) {
        case H:
            if (text[count] == 'B') now = B1;
            else now = ER;
            break;
        case B1:
            if (text[count] == '⊥') now = S;
            else if (text[count] == '0') now = B0;
            else if (text[count] == '1') now = A1;
            else now = ER;
            break;
        case B0:
            if (text[count] == '1') now = A1;
            else now = ER;
            break;
        case A1:
            if (text[count] == '1') now = B1;
            else if (text[count] == '0') now = C0;
            else now = ER;
            break;
        case C0:
            if (text[count] == '1') now = B1;
            else now = ER;
            break;
        default:
            now = ER;
            break;
        }
        res += to_string(now) + " ";
        count++;
    }

    cout << res << endl;
}

int main()
{
    setlocale(LC_ALL, "RU");

    cout << "Задание 2.3" << endl;
    list<Rule> dict = {
        Rule("S", "B⊥"),
        Rule("A", "B1"),
        Rule("A", "0"),
        Rule("B", "A1"),
        Rule("B", "C1"),
        Rule("B", "B0"),
        Rule("B", "1"),
        Rule("C", "A0"),
        Rule("C", "B1")
    };

    PrintRules(dict);
    FormalLanguage fl(dict);

    take_input();
    //take_input_static();
    print_output();
    create_state_transitions(start_state);
    print_dfa();



    cout << "Анализаторы цепочек " << endl;
    cout << "Состояния: H-0, BS-1, BCS-2, B-3, ER-4" << endl;
    cout << "Цепочка 1011    \t:";
    Analizator("1011");
    cout << "Цепочка 0       \t:";
    Analizator("0");
    cout << "Цепочка 101011  \t:";
    Analizator("101011");
    cout << endl;

    cout << "G ({B, 0, 1, ⊥}, {H, B1, B0, A1, C0, S, ER}, P, H)" << endl;

    return 0;
}
