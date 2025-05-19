#include <iostream>
#include <fstream>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

void loadJSON(const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error: Could not open the file!\n";
        return;
    }

    json jsonData;
    file >> jsonData; 
    file.close();

    std::cout << "Loaded JSON:\n" << jsonData.dump(4) << "\n";
    
    std::cout << "Name: " << jsonData["contract"] << "\n";
}

int main() {
    loadJSON("data.json"); 
    return 0;
}
