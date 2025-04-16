#include "transaction.h"
#include <string>

Transaction::Transaction(const std::string& s, const std::string& r, double a)
    : sender(s), receiver(r), amount(a) {}

bool Transaction::isValid() const {
    return !sender.empty() && !receiver.empty() && amount > 0;
}

std::string Transaction::toString() const {
    return sender + "->" + receiver + ": " + std::to_string(amount);
}
