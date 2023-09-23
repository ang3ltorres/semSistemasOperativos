#include "manager.hpp"
#include <fstream>
#include <sstream>
#include <iostream>
#include <format>
#include <algorithm>

Process::Process(std::string name, unsigned int size)
: pos(0), size(size), name(name) {}

Process::Process(const std::string& string)
: pos(0)
{
	std::stringstream ss(string);
	std::getline(ss, name, ',');

	while(std::isspace(ss.peek())) ss.get();
	std::string numString;
	std::getline(ss, numString);
	size = std::stoi(numString.substr(0, numString.find_first_not_of("0123456789")));
}

std::ostream& operator<<(std::ostream& output, const Process& process)
{
	output << std::format
	(
		"{:<24s}{:<12d}{:<12d}",
		process.name, process.pos, process.size
	);

	return output;
}

bool Process::operator<(const Process& p) const
{
	return pos < p.pos;
}

std::vector<Process> processFromFile(const std::string& fileName)
{
	std::ifstream file(fileName);
	std::vector<Process> process;
	std::string line;
	while (std::getline(file, line))
		process.push_back(line);
	return process;
}

MemoryBlock::MemoryBlock(unsigned int size)
: totalSize(size) {}

std::tuple<unsigned int, unsigned int> MemoryBlock::nextFreeSpace()
{
	int index = -1;

	while (index < int(process.size()))
	{
		int i = index;
		index++;

		if (process.empty())
			return std::make_tuple(0, totalSize);

		if (i == -1)
		{
			if (process[0].pos != 0)
				return std::make_tuple(0, process[0].pos);
			else
				continue;
		}

		if (i == int(process.size() - 1))
		{
			if ((process[i].pos + process[i].size) != totalSize)
				return std::make_tuple(process[i].pos + process[i].size, totalSize - (process[i].pos + process[i].size));
			else
				continue;
		}
		else
		{
			if (process[i+1].pos - (process[i].pos + process[i].size) > 0)
				return std::make_tuple(process[i].pos + process[i].size, process[i+1].pos - (process[i].pos + process[i].size));
			else
				continue;
		}

	}
	return std::make_tuple(0, 0);
}

std::ostream& operator<<(std::ostream& output, const MemoryBlock& memoryBlock)
{
	std::cout << "Total size: " << memoryBlock.totalSize << '\n';
	for (const auto& p : memoryBlock.process)
		output << p << '\n';
	return output;
}

Manager::Manager(std::initializer_list<unsigned int> memory)
: algorithm(Algorithm::PRIMER_AJUSTE)
{
	for (const auto& i : memory)
		this->memory.push_back(MemoryBlock(i));
}

bool Manager::insertProcess(Process p)
{
	switch(algorithm)
	{
		case Algorithm::PRIMER_AJUSTE:
		{
			// Iterar entre cada bloque de memoria
			for (auto& b : memory)
			{
				auto free = b.nextFreeSpace();
				if (free != std::make_tuple(0, 0))
				{
					if (std::get<1>(free) >= p.size)
					{
						// Posicion correspondiente
						p.pos = std::get<0>(free);
						b.process.push_back(p);
						std::sort(b.process.begin(), b.process.end());
						return true;
					}
				}
			}
			return false;
		}
		break;

		default:
			throw "Algoritmo invalido";
	}
}
