#include "Scanner.h"
#include "DetectionEngine.h"
#include <iostream>

int main() {
    Scanner scanner;
    DetectionEngine detectionEngine;

    std::cout << "Starting full system scan..." << std::endl;
    scanner.fullSystemScan();

    auto threats = scanner.getThreats();
    if (threats.empty()) {
        std::cout << "No threats detected." << std::endl;
    } else {
        std::cout << "Threats detected:" << std::endl;
        for (const auto& threat : threats) {
            std::cout << threat << std::endl;
        }

        detectionEngine.fetchThreatData();
    }

    std::cout << "Press Enter to exit...";
    std::cin.get(); // Wait for user input before closing
    return 0;
}
