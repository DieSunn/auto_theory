	#pragma once
	#include <iostream>
	#include <unordered_set>
	#include <string>
	#include <list>
	#include <random>
	#include "Rule.h"
	#include <functional>

	using namespace std;

	/// ����� ����������� ����� � ������������ ����������� � ��������� �� ������������
	class FormalLanguage
	{
	private:
		/// ������� �����
		list <Rule> _rules;
		/// ����������� ���������� ����������
		int MaxRepetitionsCount;

		/// ��������� ������� �� ������������
		/// "input" - ������, � ������� ����������� �������
		/// "rule" - ������� �����
		/// "count" - ���������� ���������� ����������

		bool CheckLoop(string input, Rule rule, int count = 5) {
			for (int i = 0; i < count; i++) {
				string key = rule.getKey();
				string value = rule.getValue();

				size_t pos = input.find(key);

				if (pos != -1) // ������ -1 = npos
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

		void RefreshRules() {
			for (Rule& rule : _rules) {
				rule.setIsLooped(false);
			}
		}
	public:
		/// �����������
		FormalLanguage(list<Rule> rules, int count = 10000)
		{
			_rules = rules;
			MaxRepetitionsCount = count;
		}

		/// ������
		void setRules(list <Rule> rule)
		{
			_rules = rule;
		}

		/// ������
		list<Rule> getRules() const
		{
			return _rules;
		}

		/// ������
		void setMaxRepetitionsCount(int repeat)
		{
			MaxRepetitionsCount = repeat;
		}

		/// ������
		int getMaxRepetitionsCount()
		{
			return MaxRepetitionsCount;
		}

		/// ������������ �����.
		/// ������, ����������� �� ������ ������ �����.
		string OutputLeft()
		{
			string result = "S";
			int count = 0;
			while (count < MaxRepetitionsCount)
			{
				size_t pos = -1;

				// ������ ������� ����� �������������� ������ � �������
				for (const Rule& rule : _rules)
				{
					string key = rule.getKey();
					size_t findPos = result.find(key);
					if ((pos > findPos || pos == -1) && findPos != -1)
					{
						pos = findPos;
					}
				}

				// ���� �� ������� �������� ����������� ������� - �������
				if (pos == -1)
				{
					break;
				}

				// ������ ��� ������ ���������� ��� �������� ������ ��������������� �������
				list<Rule> rules = {};
				for (const Rule& rule : _rules)
				{
					string key = rule.getKey();
					if (pos == result.find(key))
					{
						rules.push_back(rule);
					}
				}
				// �������� ������� �������
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
			// ��������� ���������� ������ � �����������
			if (rules1.size() != rules2.size()) {
				return false;
			}
			// ��������� ������ ������� � �����������
			for (const Rule& rule1 : rules1) {
				bool found = false;
				for (const Rule& rule2 : rules2) {
					if (rule1.getKey() == rule2.getKey() && rule1.getValue() == rule2.getValue()) {
						found = true;
						break;
					}
				}
				if (!found) {
					return false;
				}
			}
			return true;
		}
		/// ��������� ������ �� ���������� ����
		/// "text" - ������ ��� ��������
		string Translate(string text)
		{
			int count = 0;
			bool isEnd = false;	// true - ���� �� ���� �� ������ �����������
			while (count < MaxRepetitionsCount)
			{
				if (isEnd) break;
				count++;
				isEnd = true;
				// ��������� �� ������� ������ ������� ����� � ������
				for (Rule& rule : _rules)
				{
					if (!rule.getIsLooped())		// ���� ������� �����������
					{
						string key = rule.getKey();
						string value = rule.getValue();
						int pos = text.find(key);
						if (pos != -1)	// ���� ���� ������
						{
							// ���� ������� ����������� ������� - ���������� ���
							if (CheckLoop(text, rule)) rule.setIsLooped(true);
							else
							{
								cout << text << endl;
								text = text.erase(pos, key.length());
								text = text.insert(pos, value);
								isEnd = false;
								break;
							}
						}
					}
					else rule.setIsLooped(!rule.getIsLooped());
				}
			}
			RefreshRules();
			return text;
		}

		void RemoveUnreachableStates(FormalLanguage& language)
		{
			// �������� ��������� ���������
			string initialState = "A";

			// ������� ��������� ��� �������� ���������� ���������
			unordered_set<string> reachableStates;

			// ����������� ������� ��� ������ ���������
			function<void(const string&)> TraverseStates = [&](const string& currentState)
				{
					// ��������� ������� ��������� � ��������� ���������� ���������
					reachableStates.insert(currentState);

					// ���� ��� �������� � ���������� ������� ���������, � ������� ����� �������
					for (const Rule& rule : language.getRules())
					{
						if (rule.getKey() == currentState)
						{
							string nextState = rule.getValue();
							if (reachableStates.count(nextState) == 0)
							{
								TraverseStates(nextState);
							}
						}
					}
				};

			// �������� ����� �� ���������� ���������
			TraverseStates(initialState);

			// ������� ����� ������ ������, ���������� ������ ���������� ��������� � ��������� � ���� ��������
			list<Rule> newRules;
			for (const Rule& rule : language.getRules())
			{
				if (reachableStates.count(rule.getKey()) != 0)
				{
					newRules.push_back(rule);
				}
			}

			// ��������� ������� ����� � ����� ������� ������
			language.setRules(newRules);
		}

	};

