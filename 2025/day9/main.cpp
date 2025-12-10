#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

struct Point {
  long x;
  long y;
};

struct VerticalLine {
  long x;
  long y1;
  long y2;
  bool operator<(const VerticalLine &other) const { return x < other.x; }
};

struct HorizontalLine {
  long y;
  long x1;
  long x2;
  bool operator<(const HorizontalLine &other) const { return y < other.y; }
};

struct Rectangle {
  long x1;
  long x2;
  long y1;
  long y2;

  long area() {
    long deltaX = std::abs(x2 - x1) + 1;
    long deltaY = std::abs(y2 - y1) + 1;
    return deltaX * deltaY;
  }
};

std::vector<Point> parsePoints() {
  std::vector<Point> points;
  std::string line;
  while (std::getline(std::cin, line)) {
    if (line.empty()) {
      continue;
    }
    std::stringstream ss(line);
    char comma;
    long x, y;
    ss >> x >> comma >> y;
    points.emplace_back(Point{x, y});
  }
  return points;
}

bool verticalOverlap(const std::vector<VerticalLine> &vertical,
                     const Rectangle &rec) {
  return std::ranges::any_of(vertical, [&](const auto &line) {
    return (line.x > rec.x1 && line.x < rec.x2) &&
           (line.y1 < rec.y2 && rec.y1 < line.y2);
  });
}

bool horizontalOverlap(const std::vector<HorizontalLine> &horizontal,
                       Rectangle rec) {
  return std::ranges::any_of(horizontal, [&](const auto &line) {
    return (line.y > rec.y1 && line.y < rec.y2) &&
           (line.x1 < rec.x2 && rec.x1 < line.x2);
  });
}

int main(int argc, char *argv[]) {

  const auto points = parsePoints();

  std::vector<VerticalLine> vertical;
  std::vector<HorizontalLine> horizontal;

  const int n = points.size();
  for (int i = 0; i < n; i++) {
    int j = (i + 1) % n;
    const Point &a = points[i];
    const Point &b = points[j];
    if (a.x == b.x) {
      vertical.emplace_back(
          VerticalLine{a.x, std::min(a.y, b.y), std::max(a.y, b.y)});
    }
    if (a.y == b.y) {
      horizontal.emplace_back(
          HorizontalLine{a.y, std::min(a.x, b.x), std::max(a.x, b.x)});
    }
  }

  long maxArea = 0;
  Rectangle maxRectangle;

  // try all valid combinations of rectangles
  for (int i = 0; i < points.size(); i++) {
    const Point &p1 = points[i];
    for (int j = i; j < points.size(); j++) {
      const Point &p2 = points[j];
      Rectangle rec = Rectangle{std::min(p1.x, p2.x), std::max(p1.x, p2.x),
                                std::min(p1.y, p2.y), std::max(p1.y, p2.y)};
      long area = rec.area();

      if (area > maxArea) {
        maxArea = area;
        maxRectangle = rec;
      }
    }
  }
  std::cout << "max area part 1: " << maxArea << "\n";

  // try all valid combinations of rectangles and check overlap
  maxArea = 0;
  for (int i = 0; i < points.size(); i++) {
    const Point &p1 = points[i];
    for (int j = i; j < points.size(); j++) {
      const Point &p2 = points[j];
      Rectangle rec = Rectangle{std::min(p1.x, p2.x), std::max(p1.x, p2.x),
                                std::min(p1.y, p2.y), std::max(p1.y, p2.y)};
      if (verticalOverlap(vertical, rec)) {
        continue;
      }
      if (horizontalOverlap(horizontal, rec)) {
        continue;
      }

      long area = rec.area();

      if (area > maxArea) {
        maxArea = area;
        maxRectangle = rec;
      }
    }
  }
  std::cout << "max area part 2: " << maxArea << "\n";
  return 0;
}
