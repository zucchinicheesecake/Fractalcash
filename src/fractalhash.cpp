#include "fractalhash.h"
#include "block.h"
#include <openssl/sha.h>
#include <cstring>
#include <sstream>
#include <iostream>
#include <iomanip>

std::string FractalHash(const Block& block, uint64_t nonce) {
    std::string data = block.merkleRoot + 
                       block.previousHash + 
                       std::to_string(block.height) + 
                       std::to_string(block.timestamp) + 
                       std::to_string(nonce);
                       
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256((const unsigned char*)data.c_str(), data.size(), hash);
    
    unsigned char hash2[SHA256_DIGEST_LENGTH];
    SHA256(hash, SHA256_DIGEST_LENGTH, hash2);
    
    std::stringstream ss;
    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        ss << std::hex << std::setw(2) << std::setfill('0') << (int)hash2[i];
    }
    return ss.str();
}

std::string generateTarget(double difficulty) {
    int leadingZeros = static_cast<int>(difficulty);
    
    std::string target(64, '0');
    
    double fraction = difficulty - leadingZeros;
    int firstNonZeroPos = leadingZeros * 2;
    
    if (firstNonZeroPos < 64) {
        int value = static_cast<int>((1.0 - fraction) * 15);
        char hexChar = value < 10 ? '0' + value : 'a' + (value - 10);
        target[firstNonZeroPos] = hexChar;
        
        for (size_t i = firstNonZeroPos + 1; i < 64; i++) {
            target[i] = 'f';
        }
    }
    
    return target;
}

bool meetsDifficulty(const std::string& hash, double difficulty) {
    std::string target = generateTarget(difficulty);
    return hash < target;
}

bool checkFractalHash(Block& block, double difficulty) {
    if (block.merkleRoot.empty()) {
        block.merkleRoot = block.calculateMerkleRoot();
    }
    
    std::string hash = FractalHash(block, block.nonce);
    return meetsDifficulty(hash, difficulty);
}
