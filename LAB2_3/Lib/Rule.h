#pragma once
#include <iostream>
#include <string>
#include <list>


using namespace std;

/// ������� �����
class Rule {
private:
	/// ����������� ������� ����� ����
	string key; 
	/// ����������� ������� ����� ��������
	string value;
	/// ������ �� ������� ������������.
	bool IsLooped;

public:
	/// �����������
	Rule(string k, string v, bool l = false) {
		key = k;
		value = v;
		IsLooped = l;
	}
	/// ����������� ������� �����
	/// ������
	void setKey(string k)
	{
		key = k;
	}
	/// ������
	string getKey() const
	{
		return key;
	}

	/// ����������� ������� �����
	/// ������
	void setValue(string v)
	{
		value = v;
	}
	/// ������
	string getValue() const
	{
		return value;
	}

	/// ������ �� ������� ������������.
	/// True - ������, false - ������� �� ����������� ����������
	/// ������
	void setIsLooped(bool l)
	{
		IsLooped = l;
	}
	/// ������
	bool getIsLooped() const
	{
		return IsLooped;
	}

	bool operator==(const Rule& other) const {
		return (getKey() == other.getKey() && getValue() == other.getValue());
	}
};

/// ����� ������ �����
void PrintRules(list<Rule>& R)
{
	cout << "������� ��� �����" << endl;

	for (const Rule& rule : R)
	{
		cout << "   " + rule.getKey() + "-->" + rule.getValue() << endl;
	}
};

