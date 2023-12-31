#pragma once
#include <string>

namespace console
{
	std::string colorF(unsigned char r, unsigned char g, unsigned char b);
	std::string colorB(unsigned char r, unsigned char g, unsigned char b);
	void clear();
	extern const std::string reset;
}
