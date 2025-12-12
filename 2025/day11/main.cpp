#include <cstdio>
#include <deque>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using Graph = std::unordered_map<std::string, std::vector<std::string>>;

Graph parseGraph() {
  std::string line;
  int totalEdges = 0;
  std::unordered_map<std::string, std::vector<std::string>> graph;
  while (std::getline(std::cin, line)) {
    if (line.empty()) {
      continue;
    }

    std::stringstream ss(line);

    std::string token;
    std::string label;
    std::vector<std::string> edges;
    while (std::getline(ss, token, ' ')) {
      if (token.back() == ':') {
        label = token.substr(0, token.size() - 1);
        continue;
      }
      edges.push_back(token);
      totalEdges++;
    }
    graph.insert({label, edges});
  }
  std::cout << "total nodes: " << graph.size() << "\n";
  std::cout << "total edges: " << totalEdges << "\n";
  return graph;
}

void dfs(const std::string &node, const Graph &graph,
         std::unordered_set<std::string> &visited,
         std::deque<std::string> &order) {
  visited.insert(node);
  auto it = graph.find(node);
  if (it != graph.end()) {
    auto &edges = it->second;
    for (auto &edge : edges) {
      if (visited.find(edge) == visited.end()) {
        dfs(edge, graph, visited, order);
      }
    }
  }
  order.push_back(node);
  return;
}

std::deque<std::string> topologicalSort(const Graph &graph,
                                        const std::string start) {
  std::deque<std::string> order;
  std::unordered_set<std::string> visited;
  dfs(start, graph, visited, order);
  return order;
}

long solvePaths(const Graph &graph, std::deque<std::string> order,
                const std::string start, const std::string end) {
  std::unordered_map<std::string, long> dp;
  dp.insert({start, 1});

  while (!order.empty()) {
    auto curr = order.back();
    if (curr == end) {
      break;
    }
    order.pop_back();
    auto it = graph.find(curr);
    if (it == graph.end()) {
      continue;
    }
    auto &edges = it->second;
    for (auto &e : edges) {
      dp[e] = dp[e] + dp[curr];
    }
  }
  return dp[end];
}

int main(int argc, char *argv[]) {
  // graph is a dag
  Graph graph = parseGraph();

  const std::string you = "you";
  const std::string out = "out";
  const std::string dac = "dac";
  const std::string fft = "fft";
  const std::string svr = "svr";

  auto order = topologicalSort(graph, you);
  std::cout << "part 1" << " -> " << solvePaths(graph, order, you, out) << "\n";

  order = topologicalSort(graph, svr);
  long svr_to_fft = solvePaths(graph, order, svr, fft);
  long fft_to_dac = solvePaths(graph, order, fft, dac);
  long dac_to_out = solvePaths(graph, order, dac, out);
  std::cout << "part 2" << " -> " << svr_to_fft * fft_to_dac * dac_to_out
            << "\n";
  return 0;
}
