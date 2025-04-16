#include "transaction_subset.h"
#include <fstream>
#include <vector>

void validateTransactionSubset(const std::vector<Transaction>& txs, int count) {
    int validCount = 0;
    for (int i = 0; i < count && i < static_cast<int>(txs.size()); i++) {
        if (txs[i].isValid()) validCount++;
    }
    
    std::ofstream log("node.log", std::ios::app);
    log << "Validated " << validCount << " out of " << 
        std::min(count, static_cast<int>(txs.size())) << " transactions\n";
}
