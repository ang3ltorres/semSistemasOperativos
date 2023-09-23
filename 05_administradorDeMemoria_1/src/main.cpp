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
	
	manager.algorithm = Algorithm::MEJOR_AJUSTE;
	auto process = processFromFile("./archivos.txt");
	manager.insertProcess(process);
	std::cout << manager;

	return 0;
}