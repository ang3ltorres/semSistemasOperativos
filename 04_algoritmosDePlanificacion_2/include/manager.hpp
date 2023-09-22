#pragma once
#include "process.hpp"
#include <string>
#include <vector>

struct Manager
{
	Manager();

	enum class Algorithm: unsigned int
	{
		RR = 0,
		SFJ,
		FIFO,
		PRIOR,
	};
	static Algorithm algorithm;

	void loadProcessFromFile(const std::string fileName);
	void consume();	
	std::vector<Process> process;
	unsigned int index;
};
