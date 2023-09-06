#include "process.hpp"

#include <iostream>
#include <format>

std::istream& operator>>(std::istream& input, Process& process)
{
	// Name
	if (!std::getline(input, process.name, ','))
		return input;
	std::string aux;

	// Time
	std::getline(input, aux, ',');
	process.time = std::stoi(aux, nullptr, 10);

	// Priority
	std::getline(input, aux);
	process.priority = std::stoi(aux, nullptr, 10);

	return input;
}

std::ostream& operator<<(std::ostream& output, const Process& process)
{
	output << std::format
	(
		"{:<25s}{:<12s}{:02d}",
		process.name, std::format("{:04d}", process.time), process.priority
	);

	return output;
}
