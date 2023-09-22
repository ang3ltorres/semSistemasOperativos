#include "process.hpp"

#include <iostream>
#include <format>
#include <thread>
#include <chrono>

Process::OrderBy Process::orderBy = Process::OrderBy::priority;

Process::Process(unsigned int time, unsigned int priority, const std::string& name)
: time(time), priority(priority), name(name) {}

Process::Process(const std::string& string)
{
	std::istringstream iss(string);

	// Name
	std::getline(iss, name, ',');
	std::string aux;

	// Time
	std::getline(iss, aux, ',');
	time = std::stoi(aux, nullptr, 10);

	// Priority
	std::getline(iss, aux);
	priority = std::stoi(aux, nullptr, 10);
}

std::ostream& operator<<(std::ostream& output, const Process& process)
{
	output << std::format
	(
		"{:<24s}{:<10s}{:02d}",
		process.name, std::format("{:04d}", process.time), process.priority
	);

	return output;
}

bool Process::operator<(const Process& p) const
{
	switch (Process::orderBy)
	{
		case Process::OrderBy::time:
			return (time != p.time) ? time < p.time : name < p.name;
			
		case Process::OrderBy::priority:
			return (priority != p.priority) ? priority < p.priority : name < p.name;

		case Process::OrderBy::name:
			return name < p.name;

		default:
			return false;
	}
}

void Process::consume(unsigned int ms)
{
	std::this_thread::sleep_for(std::chrono::milliseconds(ms));
	time--;
}
