
#include <cmath>
#include <cstdio>
#include <fstream>
#include <string>
#include <vector>
using namespace std;

int getDigit(std::string str, int i) { return str.at(i) - '0'; }

long long getJoltage(std::string str, int digits[], int numDigits) {
  long long joltage = 0;
  for (int i = 0; i < numDigits; i++) {
    joltage += getDigit(str, digits[i]) * std::pow(10, numDigits - i - 1);
  }
  return joltage;
}

void solve(int numDigits) {
  std::vector<std::vector<int>> banks;
  std::string bankStr;
  ifstream file("input.txt");
  long long sum = 0;
  while (std::getline(file, bankStr)) {
    if (bankStr.empty()) {
      continue;
    }

    int digits[numDigits];
    for (int i = 0; i < numDigits; i++) {
      digits[i] = -1;
    }
    for (int k = 0; k < numDigits; k++) {
      int r = numDigits - 1 - k;

      int start = k == 0 ? 0 : digits[k - 1] + 1;

      for (int i = start; i < bankStr.length() - r; ++i) {
        int d = getDigit(bankStr, i);
        if (digits[k] == -1 || d > getDigit(bankStr, digits[k])) {
          digits[k] = i;
        }
      }
    }
    sum += getJoltage(bankStr, digits, numDigits);
  }
  file.close();
  printf("joltage sum: %lld \n", sum);
}

int main(int argc, char *argv[]) {
  solve(2);
  solve(12);
  return 0;
}
