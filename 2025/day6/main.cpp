#include <algorithm>
#include <cctype>
#include <cstdio>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

std::vector<std::string> split(const std::string &str) {
  std::vector<std::string> tokens;
  std::istringstream iss(str);
  std::string token;

  while (iss >> token) {
    tokens.push_back(token);
  }

  return tokens;
}

void part1() {
  std::string line;

  std::vector<char> operands;
  std::vector<std::vector<int>> problems;
  while (getline(std::cin, line)) {
    if (line.empty()) {
      continue;
    }
    std::vector<int> numbers;
    for (std::string n : split(line)) {
      if (n == "+" || n == "*") {
        operands.push_back(n[0]);
        continue;
      }
      numbers.push_back(std::stoi(n));
    }
    if (numbers.size()) {
      problems.push_back(numbers);
    }
  }
  long answer = 0;
  for (int j = 0; j < problems[0].size(); ++j) {
    long result = 0;
    char op = operands[j];
    for (int i = 0; i < problems.size(); ++i) {
      int n = problems[i][j];
      if (op == '+' || result == 0) {
        result += n;
      } else {
        result *= n;
      }
    }
    answer += result;
  }
  printf("part 1: %ld \n", answer);
}

std::vector<char> splitCols(const std::string &str) {
  std::vector<char> cols;
  int i = 0;
  while (i < str.size()) {
    char c = str[i];
    cols.push_back(c);
    i++;
  }
  return cols;
}

using Grid = std::vector<std::vector<char>>;

std::vector<std::pair<char, int>> parseOperands(Grid grid) {
  std::vector<std::pair<char, int>> operands;

  int problemSize = 0;
  char op;
  int r = grid.size() - 1;
  for (int j = grid[r].size() - 1; j >= 0; --j) {
    char c = grid[r][j];
    if (std::isspace(c)) {
      if (j == grid[r].size() - 1 || std::isspace(grid[r][j + 1])) {
        problemSize++;
      }
      continue;
    }
    operands.emplace_back(c, problemSize + 1);
    problemSize = 0;
  }
  std::reverse(operands.begin(), operands.end());
  return operands;
}

void part2() {
  std::string line;

  Grid grid;
  while (getline(std::cin, line)) {
    if (line.empty()) {
      continue;
    }
    auto cols = splitCols(line);
    grid.push_back(cols);
  }

  auto operands = parseOperands(grid);
  grid.pop_back();
  std::vector<std::vector<int>> problems;

  long answer = 0;
  int k = 0;
  for (auto &op : operands) {
    long result = 0;
    for (int j = k; j < k + op.second; j++) {
      std::string numStr;
      for (int i = 0; i < grid.size(); i++) {
        numStr += grid[i][j];
      }
      int n = std::stoi(numStr);
      if (op.first == '+' || result == 0) {
        result += n;
      } else {
        result *= n;
      }
    }
    answer += result;
    k += op.second + 1;
  }
  printf("part 2: %ld \n", answer);
}

int main(int argc, char *argv[]) {
  // part1();
  part2();

  return 0;
}
