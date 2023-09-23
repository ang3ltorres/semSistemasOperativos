#pragma once
#include <vector>
#include <string>
#include <tuple>

struct Process
{
	Process(std::string name, unsigned int size);
	Process(const std::string& string);

	unsigned int pos;
	unsigned int size;
	std::string name;

	friend std::ostream& operator<<(std::ostream& output, const Process& process);
	bool operator<(const Process& p) const;
};

std::vector<Process> processFromFile(const std::string& fileName);

struct MemoryBlock
{
	MemoryBlock(unsigned int size);
	unsigned int totalSize;
	std::vector<Process> process;
	std::tuple<unsigned int, unsigned int> nextFreeSpace(int& index);

	friend std::ostream& operator<<(std::ostream& output, const MemoryBlock& memoryBlock);
};

enum Algorithm: unsigned int
{
	PRIMER_AJUSTE = 0,
	MEJOR_AJUSTE,
	PEOR_AJUSTE,
	SIGUIENTE_AJUSTE,
};

using FreeSpaceInfo = std::tuple<unsigned int, unsigned int, std::reference_wrapper<MemoryBlock>>;
using LastPosition = std::tuple<int, unsigned int>;

struct Manager
{
	Manager(std::initializer_list<unsigned int> memory);
	Algorithm algorithm;
	LastPosition lastPosition;
	std::vector<MemoryBlock> memory;
	std::vector<FreeSpaceInfo> getAllFreeSpace();
	bool insertProcess(Process process);
};
