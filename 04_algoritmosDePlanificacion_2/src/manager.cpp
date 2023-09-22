#include "manager.hpp"

#include <fstream>
#include <algorithm>

Manager::Algorithm Manager::algorithm = Manager::Algorithm::DEFAULT;

Manager::Manager()
: index(0), consumePerProcess(3), currentConsumeCount(consumePerProcess) {}

void Manager::loadProcessFromFile(const std::string fileName)
{
	std::ifstream file(fileName);
	std::string line;

	while (std::getline(file, line))
		process.push_back(Process(line));
	file.close();
}

void Manager::setAlgorithm(Algorithm algorithm)
{
	Manager::algorithm = algorithm;

	if (Manager::algorithm == Manager::Algorithm::SFJ)
	{
		Process::orderBy = Process::OrderBy::time;
		std::sort(process.begin(), process.end());
	}
	else if ((Manager::algorithm == Manager::Algorithm::PRIOR) or (Manager::algorithm == Manager::Algorithm::RR))
	{
		Process::orderBy = Process::OrderBy::priority;
		std::sort(process.begin(), process.end());
	}

}

bool Manager::consume()
{
	if (process.empty())
		return false;

	if (Manager::algorithm == Manager::Algorithm::RR)
	{

		if (currentConsumeCount)
			currentConsumeCount--;
		else
		{
			currentConsumeCount = consumePerProcess - 1;
			index++;
			index = (index >= process.size()) ? 0 : index;
		}

		auto it = process.begin() + index;
		it->consume();
		if (!it->time)
		{
			process.erase(it);
			index--;
			currentConsumeCount = 0;
		}
	}
	else
	{
		auto it = process.begin();
		it->consume();
		if (!it->time)
			process.erase(it);
	}

	return true;
}