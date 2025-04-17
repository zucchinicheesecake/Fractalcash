#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>
#include <sstream>

struct Block {
    int index;
    std::string prevHash;
    std::string data;
    std::string hash;

    Block(int idx, const std::string& prev, const std::string& d)
        : index(idx), prevHash(prev), data(d), hash("dummyhash" + std::to_string(idx)) {}
};

int main() {
    std::unordered_map<std::string, int> accounts;
    std::vector<Block> blockchain;
    accounts["miner"] = 0;

    std::string input;
    while (true) {
        std::cout << "Enter command: ";
        std::getline(std::cin, input);

        std::istringstream iss(input);
        std::string cmd, arg1, arg2;
        int amount;

        iss >> cmd;

        if (cmd == "exit") break;
        else if (cmd == "generate") {
            accounts["miner"] += 50;
            std::cout << "Generated 50 coins for miner\n";
        }
        else if (cmd == "balance") {
            iss >> arg1;
            if (accounts.count(arg1)) std::cout << "Balance for " << arg1 << ": " << accounts[arg1] << "\n";
            else std::cout << "No such account.\n";
        }
        else if (cmd == "transfer") {
            iss >> arg1 >> arg2 >> amount;
            if (accounts.count(arg1) && accounts[arg1] >= amount) {
                accounts[arg1] -= amount;
                accounts[arg2] += amount;
                std::cout << "Transferred " << amount << " from " << arg1 << " to " << arg2 << "\n";
            } else {
                std::cout << "Insufficient funds or invalid account.\n";
            }
        }
        else if (cmd == "mine") {
            std::string data = "miner rewarded";
            std::string prev = blockchain.empty() ? "genesis" : blockchain.back().hash;
            Block b(blockchain.size(), prev, data);
            blockchain.push_back(b);
            std::cout << "Mined block: " << b.hash << "\n";
        }
        else {
            std::cout << "Unknown command.\n";
        }
    }
    return 0;
}
