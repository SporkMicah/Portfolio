#include "Scanner.h"
#include <iostream>
#include <filesystem>
#include <fstream>

namespace fs = std::filesystem;

void Scanner::fullSystemScan() {
    threats.clear();
    scanDirectory(fs::current_path().string());
}

void Scanner::scanDirectory(const std::string& path) {
    try {
        for (const auto& entry : fs::recursive_directory_iterator(path)) {
            if (fs::is_regular_file(entry.status())) {
                std::string filePath = entry.path().string();
                std::ifstream file(filePath);
                if (file.is_open()) {
                    std::string content((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
                    if (content.find("malicious") != std::string::npos) { // Simple detection logic
                        threats.push_back(filePath);
                    }
                }
            }
        }
    } catch (const fs::filesystem_error& e) {
        std::cerr << "Error accessing: " << e.path1() << " " << e.what() << std::endl;
    }
}

std::vector<std::string> Scanner::getThreats() const {
    return threats;
}
