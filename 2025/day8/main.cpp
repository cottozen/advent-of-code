#include <algorithm>
#include <cmath>
#include <cstddef>
#include <cstdio>
#include <iostream>
#include <numeric>
#include <queue>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

struct Point {
  int x;
  int y;
  int z;
};

struct Edge {
  int i;
  int j;
  size_t dist;

  bool operator<(const Edge &other) const { return dist < other.dist; }
};

size_t dist(const Point &p1, const Point &p2) {
  auto square = [](int a, int b) { return std::pow(a - b, 2); };
  return square(p1.x, p2.x) + square(p1.y, p2.y) + square(p1.z, p2.z);
}

class DSU {
public:
  DSU(size_t n) {
    numSets = n;
    parent.resize(n);
    std::iota(parent.begin(), parent.end(), 0);
    rank.assign(n, 1);
    size.assign(n, 1);
  }
  int find(int v) {
    if (v != parent[v]) {
      // path compression;
      parent[v] = find(parent[v]);
    }
    return parent[v];
  }
  void unite(int x, int y) { link(find(x), find(y)); }

  const int getNumSets() { return numSets; }

  std::priority_queue<std::pair<int, int>> getCircuits() {
    // get biggest circuits
    std::priority_queue<std::pair<int, int>> pq;
    for (int i = 0; i < parent.size(); i++) {
      pq.emplace(size[i], i);
    }
    return pq;
  }

private:
  int numSets;
  std::vector<int> parent;
  std::vector<int> rank;
  std::vector<int> size;

  void resize(int a, int b) {
    size[a] += size[b];
    size[b] = 0;
  }

  void link(int x, int y) {
    if (x == y) {
      return;
    }
    numSets--;
    // union by rank
    if (rank[x] > rank[y]) {
      parent[y] = x;
      resize(x, y);
    } else {
      parent[x] = y;
      resize(y, x);
      if (rank[x] == rank[y]) {
        rank[y]++;
      }
    }
  }
};

std::vector<Point> parsePoints() {
  std::vector<Point> points;
  std::string line;
  int i = 0;
  while (std::getline(std::cin, line)) {
    if (line.empty()) {
      continue;
    }
    std::stringstream ss(line);
    char comma;
    int x, y, z;
    ss >> x >> comma >> y >> comma >> z;
    points.emplace_back(Point{x, y, z});
    i++;
  }
  return points;
}

int main(int argc, char *argv[]) {

  const int n = 1000;
  const int m = 3;

  const std::vector<Point> points = parsePoints();
  const int numPoints = points.size();

  DSU dsu{points.size()};

  std::vector<Edge> edges;
  edges.reserve(numPoints * numPoints / 2);
  for (int i = 0; i < numPoints; i++) {
    for (int j = i + 1; j < numPoints; j++) {
      size_t d = dist(points[i], points[j]);
      edges.emplace_back(Edge{i, j, d});
    }
  }
  // sort edges and unite top n
  std::sort(edges.begin(), edges.end());
  std::cout << "computed distances \n";
  for (int i = 0; i < n; i++) {
    auto &egde = edges[i];
    dsu.unite(egde.i, egde.j);
  }

  // get circuits as priority queue
  auto circuits = dsu.getCircuits();
  // compute result
  size_t result = 1;
  for (int k = 0; k < m; k++) {
    auto c = circuits.top();
    circuits.pop();
    result *= c.first;
  }
  printf("part 1: %ld \n", result);

  for (int i = n; i < edges.size(); i++) {
    auto &edge = edges[i];
    dsu.unite(edge.i, edge.j);
    if (dsu.getNumSets() == 1) {
      printf("part 2: %d \n", points[edge.i].x * points[edge.j].x);
      break;
    }
  }

  return 0;
}
