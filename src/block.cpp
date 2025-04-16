#include "block.h"
#include "fractalhash.h"
#include <openssl/sha.h>
#include <sstream>
#include <chrono>
#include <iomanip>

Block::Block(int h, const std::string& prevHash) 
    : height(h), pendingTxs(0), previousHash(prevHash) {
    timestamp = std::chrono::duration_cast<std::chrono::seconds>(
        std::chrono::system_clock::now().time_since_epoch()).count();
}

std::string Block::calculateMerkleRoot() const {
    if (transactions.empty()) {
        return "0000000000000000000000000000000000000000000000000000000000000000";
    }
    
    std::vector<std::string> hashes;
    
    for (const auto& tx : transactions) {
        unsigned char hash[SHA256_DIGEST_LENGTH];
        std::string txData = tx.toString();
        SHA256((const unsigned char*)txData.c_str(), txData.size(), hash);
        
        std::stringstream ss;
        for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
            ss << std::hex << std::setw(2) << std::setfill('0') << (int)hash[i];
        }
        hashes.push_back(ss.str());
    }
    
    while (hashes.size() > 1) {
        if (hashes.size() % 2 != 0) {
            hashes.push_back(hashes.back());
        }
        
        std::vector<std::string> newHashes;
        for (size_t i = 0; i < hashes.size(); i += 2) {
            std::string concat = hashes[i] + hashes[i + 1];
            unsigned char hash[SHA256_DIGEST_LENGTH];
            SHA256((const unsigned char*)concat.c_str(), concat.size(), hash);
            
            std::stringstream ss;
            for (int j = 0; j < SHA256_DIGEST_LENGTH; j++) {
                ss << std::hex << std::setw(2) << std::setfill('0') << (int)hash[j];
            }
            newHashes.push_back(ss.str());
        }
        
        hashes = newHashes;
    }
    
    return hashes[0];
}

std::string Block::calculateHash() const {
    std::string root = merkleRoot.empty() ? calculateMerkleRoot() : merkleRoot;
    return FractalHash(*this, nonce);
}
