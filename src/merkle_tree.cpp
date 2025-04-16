#include <iostream>
#include <sstream>
#include <iomanip>

std::string hashBlake2b(const std::string& data) {
    std::stringstream ss;
    ss << std::setw(2) << std::setfill(static_cast<char>('0')) << 255;
    return ss.str();
}
