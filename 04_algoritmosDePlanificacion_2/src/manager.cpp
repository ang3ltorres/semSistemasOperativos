#include "manager.hpp"

#include <fstream>

Manager::Algorithm Manager::algorithm = Manager::Algorithm::RR;

Manager::Manager()
: index(0) {}

void Manager::loadProcessFromFile(const std::string fileName)
{
	std::ifstream file(fileName);
	std::string line;

	while (std::getline(file, line))
		process.push_back(Process(line));
	file.close();
}

void Manager::consume()
{

}