
#include <sstream>

#include "mylib.h"

Elem::~Elem() {}

void Elem::print(std::ostream& s) const
{
  s<<printstr();
}

std::string Elem::printstr() const
{
    std::ostringstream s;
    s<<"Generic element: "<<name<<"\n";
    return s.str();
}

Special::Special()
  :Elem()
  ,foo()
{
  for(size_t i=0; i<6; i++)
    vals[i] = 2*i;
}

void Special::print(std::ostream& s) const
{
    s<<"Special element: "<<name<<"\n"
     <<" "<<foo<<"\n"
     <<" vals:";
    for(size_t i=0; i<6; i++) {
        if(i!=0) s<<", ";
        s<<vals[i];
    }
    s<<"\n";
}

Special::~Special() {}

Cell::Cell()
 :elem()
{}

std::string Line::tostring() const
{
    std::ostringstream strm;
    strm<<"Line with "<<cells.size()<<" elements\n";
    for(std::vector<Cell>::const_iterator it=cells.begin(), end=cells.end();
        it!=end; ++it)
    {
        if(it->elem==NULL)
            strm<<"NULL Element\n";
        else
            it->elem->print(strm);
    }
    return strm.str();
}
