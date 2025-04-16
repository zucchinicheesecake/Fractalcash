#pragma once
#include <vector>
#include <string>
#include <cstdint>
#include "transaction.h"

struct Block {
    int height;
    int pendingTxs;
    std::vector<Transaction> transactions;
    std::string merkleRoot;
    std::string previousHash;
    uint64_t nonce = 0;
    uint64_t timestamp;

    Block(int h = 0, const std::string& prevHash = "0");
    std::string calculateMerkleRoot() const;
    std::string calculateHash() const;
};

bool checkFractalHash(Block& block, double difficulty);
