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

std::tuple<unsigned int, unsigned int> MemoryBlock::nextFreeSpace(int& index)
{
	while (index < int(process.size()))
	{
		if (process.empty())
		{
			index++;
			return std::make_tuple(0, totalSize);
		}

		if (index == -1)
		{
			index++;
			if (process[0].pos != 0)
				return std::make_tuple(0, process[0].pos);
		}

		if (index == int(process.size()) - 1)
		{
			if ((process[index].pos + process[index].size) != totalSize)
			{
				index++;
				return std::make_tuple(process[index-1].pos + process[index-1].size, totalSize - (process[index-1].pos + process[index-1].size));
			}
			else
			{
				index++;
				continue;
			}
		}
		else
		{
			if (process[index+1].pos - (process[index].pos + process[index].size) > 0)
			{
				index++;
				return std::make_tuple(process[index-1].pos + process[index-1].size, process[index].pos - (process[index-1].pos + process[index-1].size));
			}
			else
			{
				index++;
				continue;
			}
		}

	}
	return std::make_tuple(0, 0);
}

std::ostream& operator<<(std::ostream& output, const MemoryBlock& memoryBlock)
{
	for (const auto& p : memoryBlock.process)
		output << p << "\n";
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
				int index = -1;
				auto free = b.nextFreeSpace(index);
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
