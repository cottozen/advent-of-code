#include <cmath>
#include <cstdio>
#include <fstream>
#include <set>
#include <vector>

using namespace std;

struct Range {
  long long lower;
  long long upper;
};

std::vector<Range> getRanges() {
  std::vector<Range> ranges;
  std::string rangeStr;
  ifstream file("input.txt");
  while (std::getline(file, rangeStr, ',')) {
    if (rangeStr.empty()) {
      continue;
    }

    size_t dashPos = rangeStr.find('-');
    if (dashPos != std::string::npos) {
      long long start = std::stoll(rangeStr.substr(0, dashPos));
      long long end = std::stoll(rangeStr.substr(dashPos + 1));
      ranges.emplace_back(Range{start, end});
    }
  }
  file.close();
  return ranges;
}
int digitCount(long long n) {
  if (n == 0)
    return 1;
  return std::log10(std::abs(n)) + 1;
}

long long copySeq(long long seq, int d, int i) {
  long long clone = 0;
  for (int j = 0; j < d; j += i) {
    clone += seq * std::pow(10, j);
  }
  return clone;
}
void part1(std::vector<Range> &ranges) {
  long long sum = 0;
  std::set<long long> invalid;
  for (Range &r : ranges) {
    int dLower = digitCount(r.lower);
    int dUpper = digitCount(r.upper);
    for (int d = dLower; d <= dUpper; d++) {
      if (d % 2 != 0) {
        continue;
      }
      int i = d / 2;
      long long baseSeq = std::pow(10, i - 1);
      long long maxSeq = copySeq(9, i, 1);

      for (long long seq = baseSeq; seq <= maxSeq; ++seq) {
        long long clone = copySeq(seq, d, i);
        if (invalid.count(clone) == 0 && r.lower <= clone && clone <= r.upper) {
          sum += clone;
          invalid.insert(clone);
        }
      }
    }
  }
  printf("part1 sum: %lld \n", sum);
}

void part2(std::vector<Range> &ranges) {
  long long sum = 0;
  std::set<long long> invalid;
  for (Range &r : ranges) {
    int dLower = digitCount(r.lower);
    int dUpper = digitCount(r.upper);
    for (int d = dLower; d <= dUpper; d++) {
      for (int i = 1; i <= d / 2; i++) {
        if (d % i != 0) {
          continue;
        }
        long long baseSeq = std::pow(10, i - 1);
        long long maxSeq = copySeq(9, i, 1);

        for (long long seq = baseSeq; seq <= maxSeq; ++seq) {
          long long clone = copySeq(seq, d, i);
          if (invalid.count(clone) == 0 && r.lower <= clone &&
              clone <= r.upper) {
            sum += clone;
            invalid.insert(clone);
          }
        }
      }
    }
  }
  printf("part2 sum: %lld \n", sum);
}

int main(int argc, char *argv[]) {
  long long sum = 0;
  auto ranges = getRanges();
  part1(ranges);
  part2(ranges);
  return 0;
}
