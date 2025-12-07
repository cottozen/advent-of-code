
#include <algorithm>
#include <cstdio>
#include <iostream>
#include <ostream>
#include <stack>
#include <string>
#include <vector>

struct Point {
  long long x;
  bool is_start;
};

bool compPoint(Point a, Point b) {
  if (a.x == b.x) {
    return a.is_start;
  }

  return a.x < b.x;
}

class Interval {

public:
  Interval(long long start, long long end) : start(start), end(end) {}

  long long start;
  long long end;

  bool contains(long long x) { return start <= x && x <= end; }
};

void readInput(std::vector<Interval> &intervals, std::vector<long long> &ids) {
  std::string intervalStr;
  while (std::getline(std::cin, intervalStr)) {
    if (intervalStr.empty()) {
      continue;
    }
    size_t dashPos = intervalStr.find('-');
    if (dashPos != std::string::npos) {
      long long start = std::stoll(intervalStr.substr(0, dashPos));
      long long end = std::stoll(intervalStr.substr(dashPos + 1));
      intervals.emplace_back(Interval{start, end});
    } else {
      long long id = std::stoll(intervalStr);
      ids.push_back(id);
    }
  }
}

long long getRange(std::vector<Interval> &intervals) {
  std::vector<Point> points;
  for (Interval interval : intervals) {
    points.emplace_back(Point{interval.start, true});
    points.emplace_back(Point{interval.end, false});
  }
  std::sort(points.begin(), points.end(), compPoint);

  long long totalRange = 0;
  std::stack<Point> stack;
  for (auto &p : points) {
    if (p.is_start) {
      stack.push(p);
      continue;
    }
    auto pStart = stack.top();
    stack.pop();
    if (stack.empty()) {
      totalRange += p.x - pStart.x + 1;
    }
  }
  return totalRange;
}

int main(int argc, char *argv[]) {

  std::vector<Interval> intervals;
  std::vector<long long> ids;
  readInput(intervals, ids);
  int numFresh = 0;
  int freshRanges = 0;

  for (long long id : ids) {
    for (Interval interval : intervals) {
      if (interval.contains(id)) {
        numFresh++;
        break;
      }
    }
  }
  std::cout << "num fresh : " << numFresh << "\n";

  long long totalRange = getRange(intervals);
  std::cout << "range: " << totalRange << "\n";

  return 0;
}
