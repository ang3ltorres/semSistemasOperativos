#pragma once

#include <string>
#include <istream>

struct Process
{
	Process(unsigned int time, unsigned int priority, const std::string& name);
	Process(const std::string& string);

	enum class OrderBy: unsigned int
	{
		time = 0,
		priority,
		name,
	};
	static OrderBy orderBy;

	unsigned int time;
	unsigned int priority;
	std::string name;

	friend std::ostream& operator<<(std::ostream& output, const Process& process);

	bool operator<(const Process& p) const;

	void consume(unsigned int ms);
};