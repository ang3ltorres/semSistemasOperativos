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
		DEFAULT,
	};
	static Algorithm algorithm;

	void loadProcessFromFile(const std::string fileName);
	void setAlgorithm(Algorithm algorithm);
	bool consume();	
	std::vector<Process> process;
	unsigned int index;
	unsigned int consumePerProcess;
	unsigned int currentConsumeCount;
};
