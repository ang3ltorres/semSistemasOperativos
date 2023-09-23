#include <iostream>

#include "manager.hpp"

int main()
{
	Manager manager
	{
		1000,
		400,
		1800,
		700,
		900,
		1200,
		1500,
	};

	auto process = processFromFile("./archivos.txt");
	for (const auto& p : process)
		manager.insertProcess(p);
	
	for (unsigned int i = 0; i < manager.memory.size(); i++)
		std::cout << "Bloque de memoria: " << i << "\n" << manager.memory[i] << "\n\n";

	std::cout << "Nice";
	return 0;
}