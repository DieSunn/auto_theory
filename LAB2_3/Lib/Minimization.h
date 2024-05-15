#include <iostream>
#include <unordered_set>
#include <string>
#include <list>
#include <random>
#include <functional>
//#include "FormalLanguage.h"
#include "Rule.h"

using namespace std;

class FormalLanguage
{
private:
    list<Rule> _rules;
    int MaxRepetitionsCount;

    bool CheckLoop(string input, Rule rule, int count = 5)
    {
        for (int i = 0; i < count; i++)
        {
            string key = rule.getKey();
            string value = rule.getValue();

            size_t pos = input.find(key);

            if (pos != string::npos)
            {
                input = input.erase(pos, key.length());
                input = input.insert(pos, value);
            }
            else
            {
                return false;
            }
        }
        return true;
    }

    void RefreshRules()
    {
        for (Rule& rule : _rules)
        {
            rule.setIsLooped(false);
        }
    }

public:
    FormalLanguage(list<Rule> rules, int count = 10000)
    {
        _rules = rules;
        MaxRepetitionsCount = count;
    }

    void setRules(list<Rule> rule)
    {
        _rules = rule;
    }

    list<Rule> getRules() const
    {
        return _rules;
    }

    void setMaxRepetitionsCount(int repeat)
    {
        MaxRepetitionsCount = repeat;
    }

    int getMaxRepetitionsCount() const
    {
        return MaxRepetitionsCount;
    }

    string OutputLeft()
    {
        string result = "A";
        int count = 0;
        while (count < MaxRepetitionsCount)
        {
            size_t pos = string::npos;

            for (const Rule& rule : _rules)
            {
                string key = rule.getKey();
                size_t findPos = result.find(key);
                if ((pos > findPos || pos == string::npos) && findPos != string::npos)
                {
                    pos = findPos;
                }
            }

            if (pos == string::npos)
            {
                break;
            }

            list<Rule> rules = {};
            for (const Rule& rule : _rules)
            {
                string key = rule.getKey();
                if (pos == result.find(key))
                {
                    rules.push_back(rule);
                }
            }

            random_device random;
            mt19937 gen(random());
            uniform_int_distribution<int> dist(0, rules.size() - 1);
            int index = dist(gen);
            auto it = rules.begin();
            advance(it, index);
            Rule r = *it;
            size_t p = result.find(r.getKey());
            result = result.erase(p, r.getKey().length());
            result = result.insert(p, r.getValue());
            count++;
        }
        return result;
    }

    bool CompareGrammars(const FormalLanguage& grammar1, const FormalLanguage& grammar2)
    {
        list<Rule> rules1 = grammar1.getRules();
        list<Rule> rules2 = grammar2.getRules();

        if (rules1.size() != rules2.size())
        {
            return false;
        }

        for (const Rule& rule1 : rules1)
        {
            bool found = false;
            for (const Rule& rule2 : rules2)
            {
                if (rule1 == rule2)
                {
                    found = true;
                    break;
                }
            }
            if (!found)
            {
                return false;
            }
        }
        return true;
    }

    bool IsRegularLanguage()
    {
        unordered_set<string> reachableStates;
        unordered_set<string> oldStates;

        reachableStates.insert("A");

        while (oldStates != reachableStates)
        {
            oldStates = reachableStates;
            for (const Rule& rule : _rules)
            {
                string key = rule.getKey();
                string value = rule.getValue();

                if (reachableStates.find(key) != reachableStates.end())
                {
                    reachableStates.insert(value);
                }
            }
        }

        for (const Rule& rule : _rules)
        {
            string key = rule.getKey();
            string value = rule.getValue();
            if (reachableStates.find(key) == reachableStates.end() &&
                reachableStates.find(value) != reachableStates.end())
            {
                return false;
            }
        }

        return true;
    }

    /// ”дал€ет недостижимые состо€ни€ из грамматики
    void RemoveUnreachableStates() {
        unordered_set<string> reachableStates;
        unordered_set<string> oldStates;

        // ƒобавл€ем начальное состо€ние
        reachableStates.insert("A");

        // ѕока множество достижимых состо€ний мен€етс€, продолжаем итерации
        while (oldStates != reachableStates) {
            oldStates = reachableStates;
            for (const Rule& rule : _rules) {
                string key = rule.getKey();
                string value = rule.getValue();
                // ≈сли ключ состо€ни€ достижим, добавл€ем значение в множество достижимых состо€ний
                if (reachableStates.find(key) != reachableStates.end()) {
                    reachableStates.insert(value);
                }
            }
        }

        // ”дал€ем правила с недостижимыми состо€ни€ми
        auto it = _rules.begin();
        while (it != _rules.end()) {
            string key = it->getKey();
            if (reachableStates.find(key) == reachableStates.end()) {
                it = _rules.erase(it);
            }
            else {
                ++it;
            }
        }
    }
};