#ifndef SOLVER_H
#define SOLVER_H
#include "maze.h"
#include "cell.h"
#include <vector>

class Solver
{
 private:
  char** grid;
  Cell start;
  Cell end;

  Maze* maze;

  void find_start_and_end();
  void get_new_cell(int& row, int& col, int dir);
  bool backtrack_r(int row, int col, bool animate);
  bool is_valid(int row, int col);

 public:
  Solver(Maze* maze);
  bool backtrack(bool animate=true);
  void breadth_first_search(bool animate=true);
  void depth_first_search(bool animate=true);
};

enum
{
  EAST,
  SOUTH,
  WEST,
  NORTH
};

std::vector<Cell> get_neighbors(Cell* node, const int max_row, const int max_col);

#endif
