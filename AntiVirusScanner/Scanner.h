#ifndef SCANNER_H
#define SCANNER_H

#include <vector>
#include <string>

class Scanner {
public:
    void fullSystemScan();
    std::vector<std::string> getThreats() const;

private:
    std::vector<std::string> threats;
    void scanDirectory(const std::string& path);
};

#endif // SCANNER_H
