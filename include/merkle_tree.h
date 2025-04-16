#ifndef MERKLE_TREE_H
#define MERKLE_TREE_H
#include <string>
#include <vector>
enum HashType {SHA256=0, BLAKE2B=1, ALTERNATING=2};
struct ProofElement{std::string hash; bool isLeft;};
std::string hashSHA256(const std::string& data);
std::string hashBlake2b(const std::string& data);
std::string applyHash(const std::string& data, int level, HashType hashType);
std::string buildMerkleTree(const std::vector<std::string>& leaves, HashType hashType = SHA256);
std::vector<ProofElement> generateMerkleProof(const std::vector<std::string>& leaves, size_t index, HashType hashType = SHA256);
bool verifyMerkleProof(const std::string& rootHash, const std::string& leaf, const std::vector<ProofElement>& proof, HashType hashType = SHA256);
#endif
