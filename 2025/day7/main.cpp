#include <cmath>
#include <cstdio>
#include <iostream>
#include <string>
#include <vector>

using Grid = std::vector<std::string>;

long long dfs(Grid &grid, int i, int j, std::vector<long long> &memo,
              int cols) {
  int k = i * cols + j;
  // use memo if we have cols
  if (cols != 0 && memo[k] != -1) {
    return memo[k];
  }
  long long split_count = 0;
  if (grid[i][j] == '^') {
    split_count++;
    if (j < grid[i].size()) {
      split_count += dfs(grid, i, j + 1, memo, cols);
    }
    if (j > 0) {
      split_count += dfs(grid, i, j - 1, memo, cols);
    }
  } else if (grid[i][j] != '|') {
    grid[i][j] = '|';
    if (i < grid.size() - 1) {
      split_count += dfs(grid, i + 1, j, memo, cols);
    }
  }
  // use memo if we have cols
  if (cols != 0) {
    memo[k] = split_count;
  }
  return split_count;
}

long long part1(Grid grid, int i, int j) {
  std::vector<long long> memo;
  return dfs(grid, i, j, memo, 0);
}
long long part2(Grid &grid, int i, int j) {
  const size_t rows = grid.size();
  const size_t cols = grid[0].size();
  std::vector<long long> memo;
  memo.reserve(rows * cols);
  for (int i = 0; i < rows * cols; i++) {
    memo[i] = -1;
  }
  return dfs(grid, i, j, memo, cols) + 1;
}

int main(int argc, char *argv[]) {
  std::string line;
  std::vector<std::string> grid;
  int i = 0;
  int j = 0;
  int r = 0;
  while (std::getline(std::cin, line)) {
    if (line.empty()) {
      continue;
    }
    for (int k = 0; k < line.size(); ++k) {
      if (line[k] == 'S') {
        i = r;
        j = k;
      }
    }
    grid.push_back(line);
    r++;
  }
  std::cout << "part 1: " << part1(grid, i, j) << "\n";
  std::cout << "part 2: " << part2(grid, i, j) << "\n";
  return 0;
}
