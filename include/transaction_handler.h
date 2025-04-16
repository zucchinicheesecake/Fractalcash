#pragma once
#include <vector>
#include "block.h"
struct Transaction;

void processTransactions(std::vector<Transaction>& txs, Block& currentBlock);

