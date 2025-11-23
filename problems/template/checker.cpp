#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>

std::string readFile(const std::string& filePath) {
    std::ifstream file(filePath);
    if (!file.is_open()) {
        return "";
    }
    std::stringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}

std::string trim(const std::string& str) {
    size_t first = str.find_first_not_of(" \t\n\r");
    if (std::string::npos == first) {
        return str;
    }
    size_t last = str.find_last_not_of(" \t\n\r");
    return str.substr(first, (last - first + 1));
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        return 1;
    }

    std::string inputFile = argv[1];
    std::string outputFile = argv[2];
    std::string answerFile = argv[3];

    std::string inputContent = readFile(inputFile);
    std::string outputContent = readFile(outputFile);
    std::string answerContent = readFile(answerFile);

    if (trim(outputContent) == trim(answerContent)) {
        return 0; // Correct
    } else {
        return 1; // Incorrect
    }
}

