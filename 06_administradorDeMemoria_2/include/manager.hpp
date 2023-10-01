#pragma once
#include <vector>
#include <string>
#include <tuple>

using FreeSpaceInfo = std::tuple<unsigned int, unsigned int, unsigned int>;
using LastPosition = std::tuple<int, unsigned int>;

struct Process
{
	Process(std::string name, unsigned int size);
	Process(const std::string& string);

	unsigned int pos;
	unsigned int size;
	std::string name;

	bool operator<(const Process& p) const;
	friend std::ostream& operator<<(std::ostream& output, const Process& process);
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

struct Manager
{
	Manager(const std::vector<unsigned int>& memory);

	Algorithm algorithm;
	LastPosition lastPosition;
	std::vector<MemoryBlock> memory;
	std::vector<Process> processHistory;

	void addMemoryBlock(unsigned int size, bool end = true);
	std::vector<FreeSpaceInfo> getAllFreeSpace();
	bool insertProcess(Process p, bool addToHistory = true);
	bool insertProcess(const std::vector<Process>& process);
	void refresh();
	friend std::ostream& operator<<(std::ostream& output, const Manager& manager);
};
