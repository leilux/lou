#include <iostream>

struct Printer 
{
	Printer(const std::string& prefix, const std::string& suffix)
		:
		  prefix_(prefix),
		  suffix_(suffix)
	{
	}
	void 
	operator ()(std::ostream& out, const std::string& message)
	{
		out << prefix_ << message << suffix_;
	}
	std::string prefix_, suffix_;
};

int main()
{
	Printer printer = Printer("<<", ">>\n");
	printer(std::cout, "hello world");

	return 0;
}
