#pragma once
#include <string>
#include <istream>

struct Process
{
	unsigned int time;
	unsigned int priority;
	std::string name;

	friend std::istream& operator>>(std::istream& input, Process& process);
	friend std::ostream& operator<<(std::ostream& output, const Process& process);

	bool operator<(const Process& p) const;
};
