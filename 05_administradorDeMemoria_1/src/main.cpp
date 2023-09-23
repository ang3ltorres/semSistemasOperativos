#include <iostream>

#include "manager.hpp"

int main()
{
	Manager manager
	{
		2000,
		400,
		1800,
		700,
		900,
		1200,
		1500,
	};

	// auto process = processFromFile("./archivos.txt");

	Process p1("System", 300);
	p1.pos = 100;
	manager.memory[0].process.push_back(p1);

	Process p2("WinMain", 500);
	p2.pos = 800;
	manager.memory[0].process.push_back(p2);

	Process p3("Word", 200);
	p3.pos = 1400;
	manager.memory[0].process.push_back(p3);
	

	int index = -1;
	std::tuple<unsigned int, unsigned int> free;
	while ((free = manager.memory[0].nextFreeSpace(index)) != std::make_tuple(0, 0))
		std::cout << "POS: " << std::get<0>(free) << "\t\tSIZE: " << std::get<1>(free) << '\n';

	


	return 0;
}