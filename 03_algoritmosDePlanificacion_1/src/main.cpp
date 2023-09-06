#include "manager.hpp"

int main()
{
	Manager manager("procesos.txt");
	manager.loop();

	return 0;
}