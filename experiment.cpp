#include <cmath>
#include <fstream>
#include <iostream>
#include <random>
#include <vector>

const double M_PI = 3.14;

int main() {
  std::random_device rd;  // seed source
  std::mt19937 gen(rd()); // Mersenne Twister engine

  std::uniform_int_distribution<> dist(1, 200);

  const int centerX = 50;
  const int centerY = 50;
  const int centerZ = 50;
  const int radius = 30;

  std::ofstream file("experiment.json");

  file << "{ \"data\": [";
  // Create a sphere of 1's within the cube
  if (file.is_open()) {
    for (int x = 0; x < 100; x++) {
      for (int y = 0; y < 100; y++) {
        for (int z = 0; z < 100; z++) {
          double distance =
              std::sqrt(std::pow(x - centerX, 2) + std::pow(y - centerY, 2) +
                        std::pow(z - centerZ, 2));

          if (distance <= radius) {
            int randomNumber = dist(gen);
            if (randomNumber <= 1) { // % cahance
              file << "[" << 230 + x << ", " << 780 + y << ", " << 130 + z
                   << "],\n";
            }
          }
        }
      }
    }

    file << "]}";

    file.close(); // Always close the file when done
  }

  return 0;
}