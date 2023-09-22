#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <sstream>

#include "process.hpp"
#include "manager.hpp"

namespace py = pybind11;

PYBIND11_MODULE(processManager, m)
{
	py::enum_<Process::OrderBy>(m, "OrderBy")
		.value("time", Process::OrderBy::time)
		.value("priority", Process::OrderBy::priority)
		.value("name", Process::OrderBy::name);

	py::class_<Process>(m, "Process")
		.def(py::init<unsigned int, unsigned int, const std::string&>(),
			py::arg("time") = 1,
			py::arg("priority") = 1,
			py::arg("name") = ""
		)
		.def(py::init<const std::string&>(),
			py::arg("string")
		)
		.def_readwrite("time", &Process::time)
		.def_readwrite("priority", &Process::priority)
		.def_readwrite("name", &Process::name)
		.def("consume", &Process::consume)
		.def_readwrite_static("order_by", &Process::orderBy)
		.def("__str__", [](const Process& process)
		{
			std::ostringstream os;
			os << process;
			return os.str();
		})
		.def("__lt__", &Process::operator<);

	py::enum_<Manager::Algorithm>(m, "Algorithm")
		.value("rr", Manager::Algorithm::RR)
		.value("sfj", Manager::Algorithm::SFJ)
		.value("fifo", Manager::Algorithm::FIFO)
		.value("prior", Manager::Algorithm::PRIOR);

	py::class_<Manager>(m, "Manager")
		.def(py::init<>())
		.def_readwrite("process", &Manager::process)
		.def_readwrite("index", &Manager::index)
		.def_readwrite_static("algorithm", &Manager::algorithm)
		.def("consume", &Manager::consume)
		.def("load_process_from_file", &Manager::loadProcessFromFile);
}
