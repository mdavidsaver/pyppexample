#ifndef MYLIB_H
#define MYLIB_H

#include <boost/shared_ptr.hpp>
#include <boost/enable_shared_from_this.hpp>

#include <ostream>
#include <string>
#include <vector>

// Note: enable_shared_from_this used only to enforce
//       allocation of Elem w/ shared_ptr
struct Elem : public boost::enable_shared_from_this<Elem> {
  virtual ~Elem();
  std::string name;
  virtual void print(std::ostream&) const;
protected:
  // helper for python sub-classes to avoid
  // having to wrap std::ostream
  virtual std::string printstr() const;
};

struct Special : public Elem {
  Special();
  virtual ~Special();
  std::string foo;
  double vals[6];
  virtual void print(std::ostream&) const;
};

struct Cell {
  Cell();
  boost::shared_ptr<Elem> elem;

  // boost python wants this for vector<Cell>
  inline bool operator==(const Cell& o)
  { return elem==o.elem; }
};

struct Line {
  std::vector<Cell> cells;

  std::string tostring() const;
};


#endif // MYLIB_H

