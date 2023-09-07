#include "manager.hpp"
#include "console.hpp"
#include <fstream>
#include <thread>
#include <chrono>
#include <iostream>
#include <algorithm>

Manager::Manager(const std::string& processFile)
: it(nullptr)
{
	std::ifstream input(processFile, std::fstream::binary | std::fstream::in);

	Process p;
	while (input >> p)
		process.push_back(p);

	// Imprimir original
	std::cout << console::clear << *this;
	std::this_thread::sleep_for(std::chrono::seconds(2));

	// Imprimir ordenada
	std::sort(process.begin(), process.end());
	std::cout << console::clear << *this;
	std::this_thread::sleep_for(std::chrono::seconds(2));
	

	input.close();
}

void Manager::loop()
{
	bool finish = false;

	while (!finish)
	{
		finish = true;

		for (it = process.begin(); it != process.end();)
		{
			int sleepTime = (it->time >= 3) ? 3 : it->time;

			if (sleepTime)
			{
				finish = false;

				for (int j = 0; j < sleepTime; j++)
				{
					std::cout << console::clear << *this;
					std::this_thread::sleep_for(std::chrono::seconds(1));
					it->time--;
				}

				if (it->time)
					it++;
				else
					it = process.erase(it);
			}
		}
	}

	std::cout << console::clear << console::colorF(0, 255, 0) << "Todos los procesos finalizados\n" << console::reset;
}

std::ostream& operator<<(std::ostream& output, const Manager& manager)
{
	output << console::colorB(255, 0, 255) << console::colorF(0, 255, 255) << std::format
	(
		"{:<24s}{:<10s}{:<14s}{:s}\n",
		"Nombre", "Tiempo", "Prioridad", "Tiempo (barra)"
	)
	<< console::reset;

	for (auto p = manager.process.begin(); p != manager.process.end(); p++)
	{
		if (manager.it == p)
			output << console::colorB(0, 255, 255) << console::colorF(255, 0, 255);
		else
			output << console::colorF(0, 255, 255);

		output << *p << console::reset << console::colorF(220, 220, 220) << std::format("{:s}{:s}", std::string(12, ' '), std::string(p->time, char(219))) << console::reset << "\n";
	}
	return output;
}
