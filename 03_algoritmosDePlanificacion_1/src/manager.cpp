#include "manager.hpp"
#include <fstream>
#include <thread>
#include <chrono>
#include <iostream>

Manager::Manager(const std::string& processFile)
{
	std::ifstream input(processFile, std::fstream::binary | std::fstream::in);

	Process p;
	while (input >> p)
		process.push_back(p);

	input.close();
}

void Manager::loop()
{
	bool finish = false;

	while (!finish)
	{
		finish = true;

		for (auto& p : process)
		{
			std::cout << "\x1B[2J\x1B[H";
			std::cout << *this;

			int sleepTime = (p.time >= 3) ? 3 : p.time;
			p.time -= sleepTime;

			if (sleepTime)
			{
				std::this_thread::sleep_for(std::chrono::seconds(sleepTime));
				finish = false;
			}
		}
	}
	std::cout << "\nAll task finished\n";
}

std::ostream& operator<<(std::ostream& output, const Manager& manager)
{
	output << std::format
	(
		"{:<24s}{:<10s}{:s}\n",
		"Nombre", "Tiempo", "Prioridad"
	);

	for (const auto& p : manager.process)
		output << p << "\n";
	return output;
}
