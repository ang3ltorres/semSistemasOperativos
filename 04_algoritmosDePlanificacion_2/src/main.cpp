#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <vector>
#include <string>

namespace py = pybind11;

std::vector<std::string> getString()
{
	return std::vector<std::string>
	{
		"Texto",
		"De",
		"Ejemplo",
	};
}

PYBIND11_MODULE(processManager, m)
{
	m.def("get_string", &getString, "ejemplo");
}
