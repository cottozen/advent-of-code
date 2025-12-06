#include <cstdio>
#include <iostream>
#include <string>
#include <vector>

using Grid = std::vector<std::vector<char>>;

int count_adj_rolls(int i, int j, Grid grid) {
  int count = 0;

  bool top = i > 0;
  bool down = i < grid.size() - 1;
  bool left = j > 0;
  bool right = j < grid[i].size() - 1;

  auto is_roll = [grid](int r, int c) { return grid[r][c] == '@'; };

  // top
  count += top && is_roll(i - 1, j);
  // down
  count += down && is_roll(i + 1, j);
  // left
  count += left && is_roll(i, j - 1);
  // right
  count += right && is_roll(i, j + 1);
  // top left
  count += top && left && is_roll(i - 1, j - 1);
  // top right
  count += top && right && is_roll(i - 1, j + 1);
  // down left
  count += down && left && is_roll(i + 1, j - 1);
  // down right
  count += down && right && is_roll(i + 1, j + 1);
  return count;
}

Grid readGrid() {
  std::string rowStr;

  Grid grid;
  while (std::getline(std::cin, rowStr)) {
    if (rowStr.empty()) {
      continue;
    }

    std::vector<char> row;

    for (char c : rowStr) {
      row.push_back(c);
    }
    grid.push_back(row);
  }
  return grid;
}

int main(int argc, char *argv[]) {

  Grid grid = readGrid();

  const int MIN_COUNT = 4;

  int answer = 0;
  int removed = 0;
  do {
    removed = 0;
    for (int i = 0; i < grid.size(); ++i) {
      for (int j = 0; j < grid[i].size(); ++j) {
        if (grid[i][j] == '@' && count_adj_rolls(i, j, grid) < MIN_COUNT) {
          grid[i][j] = 'x';
          removed++;
        }
      }
    }
    answer += removed;
  } while (removed > 0);
  printf("answer -> %d\n", answer);
  return 0;
}
