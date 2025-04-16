#pragma once
#include <string>
#include <cstdint>

struct Block;

std::string FractalHash(const Block& block, uint64_t nonce);
bool meetsDifficulty(const std::string& hash, double difficulty);
std::string generateTarget(double difficulty);
