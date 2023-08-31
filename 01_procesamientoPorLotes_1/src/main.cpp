#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <vector>
#include <format>
#include <array>
#include <ranges>

std::vector<std::string> linesFromFile(const std::string& fileName)
{
	std::vector<std::string> lines;
	std::ifstream file(fileName, std::ios::binary | std::ios::in);

	std::string line;
	while (std::getline(file, line, '\n'))
		lines.push_back(line);

	file.close();
	return lines;
}

struct User
{
	std::array<unsigned char, 4> ip;
	std::array<unsigned short, 8> address;
	std::string name;

	User(const std::string& userString)
	{
		std::string aux;
		std::istringstream stream(userString);

		// Get first 8 address numbers
		for (auto& i : address)
		{
			std::getline(stream, aux, ':');
			i = std::stoi(aux, nullptr, 16);
		}

		// Get second string
		stream.seekg(0);
		for (int i : std::views::iota(0, 3))
			std::getline(stream, name, ',');

		// Start at 5th string
		stream.seekg(0);
		for (int i : std::views::iota(0, 5))
			std::getline(stream, aux, ',');

		// Get ip
		for (auto& i : ip)
		{
			std::getline(stream, aux, '.');
			i = std::stoi(aux, nullptr, 10);
		}
	}

	friend std::ostream& operator<<(std::ostream& os, const User& u)
	{
		os << std::format(
			"{:s} : {:d} : {:d} : {:d} : {:d} : {:d} : {:d} : {:d} : {:d} : {:0X}.{:0X}.{:0X}.{:0X}",
			u.name,
			u.address[0], u.address[1], u.address[2], u.address[3], u.address[4], u.address[5], u.address[6], u.address[7],
			u.ip[0], u.ip[1], u.ip[2], u.ip[3]
		);
		return os;
	}
};

int main()
{
	auto lines = linesFromFile("prueba2.txt");
	std::ofstream file("output.txt", std::ios::binary | std::ios::out | std::ios::trunc);

	for (const auto& i : lines)
	{
		User user(i);
		std::cout << user << std::endl;
		file << user << std::endl;
	}

	file.close();
	return 0;
}