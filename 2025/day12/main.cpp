#include <algorithm>
#include <bitset>
#include <cctype>
#include <climits>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

using Shape = std::vector<std::pair<int, int>>;

struct Region {
  int rows;
  int cols;
  std::vector<int> shapeIndicies;

  std::vector<int> getRequiredShapes(std::vector<Shape> shapes) {
    std::vector<int> requiredShapes;
    for (int i = 0; i < shapeIndicies.size(); i++) {
      int num = shapeIndicies[i];
      for (int n = 0; n < num; n++) {
        requiredShapes.push_back(i);
      }
    }
    return requiredShapes;
  }
};

const int SHAPE_DIM = 3;

void parseInput(std::vector<Shape> &shapes, std::vector<Region> &regions) {
  Shape shape;
  int i = 0;

  std::string line;
  while (std::getline(std::cin, line)) {
    if (line.empty()) {
      continue;
    }
    if (!line.empty() && std::isdigit(static_cast<unsigned char>(line[0]))) {
      if (line.size() > 1 && line[1] != ':') {
        std::stringstream ss(line);
        int cols, rows;
        char x, colon;
        if (ss >> cols >> x >> rows >> colon) {
          std::vector<int> regionShapes;
          int num;
          while (ss >> num) {
            regionShapes.push_back(num);
          }
          regions.push_back(Region{rows, cols, regionShapes});
        }
      }
      continue;
    }

    for (int j = 0; j < line.size(); j++) {
      if (line[j] == '#') {
        shape.push_back({i, j});
      }
    }
    i++;
    if (i == SHAPE_DIM) {
      shapes.push_back(shape);
      shape.clear();
      i = 0;
    }
  }

  if (!shape.empty()) {
    shapes.push_back(shape);
  }
}

void normalize(Shape &s, int rowMin, int colMin) {
  for (auto &p : s) {
    p.first -= rowMin;
    p.second -= colMin;
  }
  std::sort(s.begin(), s.end());
}

Shape rotate(Shape s) {
  Shape rShape(s.size());

  int colMin = INT_MAX;
  int rowMin = INT_MAX;
  for (int i = 0; i < s.size(); i++) {
    auto &p = s[i];
    std::pair<int, int> pr = {p.second, -p.first};
    rowMin = std::min(pr.first, rowMin);
    colMin = std::min(pr.second, colMin);
    rShape[i] = pr;
  }
  // normalize
  normalize(rShape, rowMin, colMin);
  return rShape;
}
Shape flip(Shape s) {
  Shape fShape(s.size());

  int colMin = INT_MAX;
  int rowMin = INT_MAX;
  for (int i = 0; i < s.size(); i++) {
    auto &p = s[i];
    std::pair<int, int> pf = {p.first, -p.second};
    rowMin = std::min(pf.first, rowMin);
    colMin = std::min(pf.second, colMin);
    fShape[i] = pf;
  }
  // normalize
  normalize(fShape, rowMin, colMin);

  return fShape;
}

std::vector<Shape> generateVariations(Shape s) {
  std::vector<Shape> versions;
  auto isDuplicate = [&](const Shape &candidate) {
    return std::any_of(
        versions.begin(), versions.end(),
        [&](const Shape &existing) { return existing == candidate; });
  };

  for (int i = 0; i < 4; i++) {
    s = rotate(s);
    if (!isDuplicate(s)) {
      versions.push_back(s);
    }
  }
  s = flip(s);
  for (int i = 0; i < 4; i++) {
    s = rotate(s);
    if (!isDuplicate(s)) {
      versions.push_back(s);
    }
  }
  return versions;
}

const size_t MAX_REGION_SIZE = 2500;
using RegionMask = std::bitset<MAX_REGION_SIZE>;

std::vector<RegionMask> generateMasks(const std::vector<Shape> &variations,
                                      int rows, int cols) {
  std::vector<RegionMask> validMasks;

  for (int i = 0; i < rows; ++i) {
    for (int j = 0; j < cols; ++j) {
      for (const auto &shape : variations) {

        int max_r = 0;
        int max_c = 0;
        for (const auto &p : shape) {
          max_r = std::max(p.first, max_r);
          max_c = std::max(p.second, max_c);
        }

        if (i + max_r < rows && j + max_c < cols) {
          RegionMask mask;
          for (const auto &p : shape) {
            int idx = (i + p.first) * cols + (j + p.second);
            mask.set(idx);
          }
          validMasks.push_back(mask);
        }
      }
    }
  }

  return validMasks;
}

bool backtrack(int shape_i, RegionMask region,
               const std::vector<int> &requiredShapes,
               const std::vector<std::vector<RegionMask>> &masks,
               int last_start) {
  // base case
  if (shape_i == masks.size()) {
    return true;
  }

  int start_i = 0;
  if (shape_i > 0 && requiredShapes[shape_i - 1] == requiredShapes[shape_i]) {
    start_i = last_start;
  }
  const auto &possibleMasks = masks[shape_i];
  for (int i = start_i; i < possibleMasks.size(); i++) {
    auto m = possibleMasks[i];
    // check collisions
    if (!(region & m).any()) {

      if (backtrack(shape_i + 1, region | m, requiredShapes, masks, i + 1)) {
        return true;
      }
    }
  }
  return false;
}

int main() {
  std::vector<Shape> shapes;
  std::vector<Region> regions;
  parseInput(shapes, regions);

  std::vector<std::vector<Shape>> variations(shapes.size());
  std::vector<int> shapeArea(shapes.size());
  for (int shape_i = 0; shape_i < shapes.size(); shape_i++) {
    shapeArea[shape_i] = shapes[shape_i].size();
    auto vars = generateVariations(shapes[shape_i]);
    variations[shape_i] = vars;
  }

  int answer = 0;
  for (int r_i = 0; r_i < regions.size(); r_i++) {
    auto &r = regions[r_i];
    std::cout << "r_i: " << r_i << "\n";
    auto requiredShapes = r.getRequiredShapes(shapes);

    int areaNeeded = 0;
    for (int shape_i : requiredShapes) {
      areaNeeded += shapeArea[shape_i];
    }
    if (areaNeeded > r.cols * r.rows) {
      // skip if not enough area
      continue;
    }
    // try solve NP hard problem with recursive backtracking
    std::vector<std::vector<RegionMask>> masks(variations.size());
    int i = 0;
    for (int shape_i : requiredShapes) {
      masks[i] = generateMasks(variations[shape_i], r.rows, r.cols);
    }
    if (backtrack(0, {0}, requiredShapes, masks, 0)) {
      answer++;
    }
  }
  std::cout << "answer: " << answer << "\n";

  return 0;
}
