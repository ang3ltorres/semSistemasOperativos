#pragma once
#include "process.hpp"
#include <string>
#include <vector>

struct Manager
{
	Manager(const std::string& processFile);
	void loop();	
	std::vector<Process> process;
	std::vector<Process>::iterator it;
	friend std::ostream& operator<<(std::ostream& output, const Manager& manager);
};
