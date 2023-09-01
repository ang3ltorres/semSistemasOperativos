#include <iostream>
#include <filesystem>
#include <string>
#include <fstream>
#include <random>
#include <tuple>

// Convertir numeros a letra mayuscula random
// Convertir letras a numeros random
void parseString(std::string& string)
{
	const auto random = [](int min, int max) -> int
	{
		static std::random_device generator;
		return std::uniform_int_distribution<int>{min, max}(generator);
	};

	for (auto& c : string)
	{
		if (std::isalpha(c))
			c = char(random(48, 57));
		else if (std::isdigit(c))
			c = char(random(65, 90));
	}
}

// Get <Directories, Filenames>
std::tuple<std::vector<std::filesystem::path>, std::vector<std::filesystem::path>> parseFolder(const std::filesystem::path& path)
{
	std::vector<std::filesystem::path> directories;
	std::vector<std::filesystem::path> filenames;

	for (const auto& i : std::filesystem::recursive_directory_iterator(path))
	{
		if (i.path().has_extension())
			filenames.push_back(i);
		else
			directories.push_back(i);
	}
	return std::make_tuple(directories, filenames);
}

void processFolder(const std::filesystem::path& path)
{
	std::string folderName = path.string();
	auto folder = parseFolder(path);

	// Crear carpetas
	for (const auto& f : std::get<0>(folder))
	{
		std::filesystem::path newDir = std::filesystem::path(folderName + "_PARSED") / f.lexically_relative(std::filesystem::path(folderName));
		std::filesystem::create_directories(newDir);
	}

	// Crear archivos
	for (const auto& f : std::get<1>(folder))
	{
		std::filesystem::path newFile = std::filesystem::path(folderName + "_PARSED") / f.lexically_relative(std::filesystem::path(folderName));

		// Input archivo original
		std::ifstream input(f, std::fstream::binary | std::fstream::in);
		std::string buffer{std::istreambuf_iterator<char>(input), std::istreambuf_iterator<char>()};
		input.close();

		// Output nuevo archivo
		std::ofstream output(newFile, std::fstream::trunc | std::fstream::binary | std::fstream::out);
		parseString(buffer);
		output << buffer;
		output.close();
	}
}

int main()
{
	std::string path;
	std::cout << "Ingresa el path de la carpeta a procesar --> ";
	std::getline(std::cin, path);
	processFolder(path);

	return 0;
}