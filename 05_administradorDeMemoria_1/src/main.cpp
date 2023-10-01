#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/iostream.h>
#include <vector>
#include <string>
#include <tuple>
#include <sstream>
#include "manager.hpp"

namespace py = pybind11;

PYBIND11_MODULE(memory_manager, m)
{
	py::class_<Process>(m, "Process")
		.def_readwrite("pos", &Process::pos)
		.def_readwrite("size", &Process::size)
		.def_readwrite("name", &Process::name)
		.def("__str__", [](const Process& process)
		{
			std::ostringstream os;
			os << process;
			return os.str();
		});

	m.def("process_from_file", &processFromFile);

	py::class_<MemoryBlock>(m, "MemoryBlock")
		.def(py::init<unsigned int>())
		.def_readonly("totalSize", &MemoryBlock::totalSize)
		.def_readonly("process", &MemoryBlock::process)
		.def("__str__", [](const MemoryBlock& memoryBlock)
		{
			std::ostringstream os;
			os << memoryBlock;
			return os.str();
		});

	py::enum_<Algorithm>(m, "Algorithm")
		.value("PRIMER_AJUSTE", PRIMER_AJUSTE)
		.value("MEJOR_AJUSTE", MEJOR_AJUSTE)
		.value("PEOR_AJUSTE", PEOR_AJUSTE)
		.value("SIGUIENTE_AJUSTE", SIGUIENTE_AJUSTE);

	py::class_<Manager>(m, "Manager")
		.def(py::init<const std::vector<unsigned int>&>())
		.def_readwrite("algorithm", &Manager::algorithm)
		.def_readwrite("memory", &Manager::memory)
		.def("insert_process", (bool (Manager::*)(const std::vector<Process>&)) &Manager::insertProcess)
		.def("add_memory", &Manager::addMemoryBlock)
		.def("__str__", [](const Manager& manager)
		{
			std::ostringstream os;
			os << manager;
			return os.str();
		});
}
