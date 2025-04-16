#pragma once
#include <string>

struct Transaction {
    std::string sender;
    std::string receiver;
    double amount;
    
    Transaction(const std::string& s = "", const std::string& r = "", double a = 0.0);
    bool isValid() const;
    std::string toString() const;
};
