#include "console.hpp"
#include <format>
#include <iostream>
#include <cstdlib>

const std::string console::reset = "\x1b[0m";

std::string console::colorF(unsigned char r, unsigned char g, unsigned char b)
{
	return std::format("\x1b[38;2;{:d};{:d};{:d}m", r, g, b);
}

std::string console::colorB(unsigned char r, unsigned char g, unsigned char b)
{
	return std::format("\x1b[48;2;{:d};{:d};{:d}m", r, g, b);
}

void console::clear()
{
	#ifdef _WIN32
		std::system("cls");
	#elif __linux__
		std::system("clear");
	#endif
}
