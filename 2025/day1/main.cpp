#include <cstdio>
#include <cstdlib>
#include <vector>

enum Direction {
  Left,
  Right,
};

struct Rotation {
  int degree;
  Direction dir;
};

int parseRotations(std::vector<Rotation> &rotations) {
  FILE *file = fopen("input.txt", "r");
  if (!file) {
    perror("Failed to open file");
    return 1;
  }
  char buffer[8];
  while (fgets(buffer, sizeof(buffer), file)) {
    char dirChar = buffer[0];
    Direction dir = dirChar == 'L' ? Direction::Left : Direction::Right;
    int degree = strtol(buffer + 1, nullptr, 10);
    rotations.emplace_back(Rotation{degree, dir});
  }
  fclose(file);
  return 0;
}

const int INITIAL_DIAL = 50;
const int DIAL_MIN = 0;
const int DIAL_MAX = 100;

int main(int argc, char *argv[]) {

  std::vector<Rotation> rotations;
  parseRotations(rotations);

  int count = 0;
  int dial = INITIAL_DIAL;
  for (Rotation &r : rotations) {
    count += r.degree / DIAL_MAX;
    int remainder = r.degree % DIAL_MAX;
    int end = dial + (r.dir == Direction::Left ? -remainder : remainder);
    if ((dial != DIAL_MIN && end < DIAL_MIN) || end > DIAL_MAX) {
      count++;
    }
    dial = (end % DIAL_MAX + DIAL_MAX) % DIAL_MAX;
    if (dial == DIAL_MIN) {
      count++;
    }
  }
  printf("Count: %d\n", count);
  return 0;
}
